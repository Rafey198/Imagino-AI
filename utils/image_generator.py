"""Hugging Face image generation with primary/fallback model support."""

from __future__ import annotations

import io
import random
from dataclasses import dataclass
from typing import Optional

import requests
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError
from PIL import Image

PRIMARY_MODEL = "black-forest-labs/FLUX.1-schnell"
FALLBACK_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

ASPECT_RATIOS = {
    "1:1": (1024, 1024),
    "16:9": (1280, 720),
    "9:16": (720, 1280),
    "4:3": (1024, 768),
    "3:4": (768, 1024),
}

STYLE_SUFFIXES = {
    "General": "high quality, detailed, professional",
    "Cinematic": "cinematic lighting, dramatic atmosphere, highly detailed, beautiful composition",
    "Realistic": "photorealistic, ultra detailed, natural lighting, 8k, sharp focus",
    "Anime": "anime style, vibrant colors, detailed illustration, studio quality",
    "Fantasy Art": "fantasy art, magical atmosphere, epic, highly detailed, painterly",
    "Digital Painting": "digital painting, rich colors, artistic, detailed brushwork",
    "3D Render": "3D render, octane render, volumetric lighting, highly detailed",
    "Cyberpunk": "cyberpunk style, neon lights, futuristic, dystopian, highly detailed",
    "Portrait": "portrait photography, shallow depth of field, professional lighting, detailed face",
    "Product Photography": "product photography, studio lighting, clean background, commercial quality",
}


@dataclass
class GenerationResult:
    """Successful image generation result."""

    image: Image.Image
    model: str
    final_prompt: str
    seed: int
    used_fallback: bool = False
    rate_limited_primary: bool = False


@dataclass
class GenerationError:
    """Failed image generation."""

    message: str
    tried_fallback: bool = False
    rate_limited: bool = False


def enhance_prompt(prompt: str, style: str) -> str:
    """Append style-specific suffix to the user prompt."""
    suffix = STYLE_SUFFIXES.get(style, STYLE_SUFFIXES["General"])
    prompt = prompt.strip()
    if not prompt:
        return prompt
    return f"{prompt}, {suffix}"


def resolve_seed(seed: int) -> int:
    """Return a random seed when -1 is provided."""
    return random.randint(0, 2**32 - 1) if seed == -1 else seed


def _is_rate_limit(error: Exception) -> bool:
    """Detect HTTP 429 rate-limit responses."""
    if isinstance(error, HfHubHTTPError):
        response = getattr(error, "response", None)
        if response is not None and response.status_code == 429:
            return True
    if isinstance(error, requests.HTTPError):
        if error.response is not None and error.response.status_code == 429:
            return True
    message = str(error).lower()
    return "429" in message or "rate limit" in message


def _is_model_loading(error: Exception) -> bool:
    """Detect model warm-up / loading states."""
    message = str(error).lower()
    return "503" in message or "loading" in message or "model is currently loading" in message


def _friendly_error(error: Exception, model: str) -> str:
    """Convert exceptions into user-friendly messages."""
    if _is_rate_limit(error):
        return f"Rate limit reached on {model}."
    if _is_model_loading(error):
        return f"{model} is warming up. Please wait a moment and try again."
    if isinstance(error, (requests.Timeout, TimeoutError)):
        return "Request timed out. The server took too long to respond."
    if isinstance(error, requests.ConnectionError):
        return "Network error. Check your internet connection and try again."
    return f"Generation failed with {model}: {error}"


def _validate_image(image: object) -> Optional[Image.Image]:
    """Ensure the API returned a valid PIL image."""
    if isinstance(image, Image.Image):
        return image
    if isinstance(image, bytes):
        return Image.open(io.BytesIO(image))
    return None


def _generate_with_model(
    client: InferenceClient,
    model: str,
    prompt: str,
    negative_prompt: str,
    width: int,
    height: int,
    num_inference_steps: int,
    guidance_scale: float,
    seed: int,
) -> Image.Image:
    """Call Hugging Face text-to-image for a single model."""
    # FLUX schnell works best with low guidance; SDXL uses guidance_scale normally.
    guidance = min(guidance_scale, 3.5) if "flux" in model.lower() else guidance_scale
    neg = negative_prompt.strip() if "flux" not in model.lower() else None

    image = client.text_to_image(
        prompt,
        model=model,
        width=width,
        height=height,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance,
        seed=seed,
        negative_prompt=neg or None,
    )

    validated = _validate_image(image)
    if validated is None:
        raise ValueError("Invalid image response from API.")
    return validated


def generate_image(
    token: str,
    prompt: str,
    negative_prompt: str = "",
    style: str = "General",
    aspect_ratio: str = "1:1",
    num_inference_steps: int = 4,
    guidance_scale: float = 7.5,
    seed: int = -1,
) -> GenerationResult | GenerationError:
    """
    Generate an image using the primary model, falling back on failure or 429.

    Returns GenerationResult on success or GenerationError on failure.
    """
    if not token or not token.strip():
        return GenerationError(
            message="HF_TOKEN is missing. Add it to your .env file and restart the app."
        )

    if not prompt or not prompt.strip():
        return GenerationError(message="Please enter a prompt before generating.")

    final_prompt = enhance_prompt(prompt, style)
    resolved_seed = resolve_seed(seed)
    width, height = ASPECT_RATIOS.get(aspect_ratio, (1024, 1024))

    client = InferenceClient(api_key=token.strip(), provider="auto")
    models = [PRIMARY_MODEL, FALLBACK_MODEL]
    errors: list[str] = []
    tried_fallback = False
    rate_limited_primary = False

    for index, model in enumerate(models):
        if index > 0:
            tried_fallback = True

        # FLUX schnell defaults to fewer steps; SDXL benefits from more.
        steps = num_inference_steps
        if "flux" in model.lower() and steps > 8:
            steps = min(steps, 8)

        try:
            image = _generate_with_model(
                client=client,
                model=model,
                prompt=final_prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                seed=resolved_seed,
            )
            return GenerationResult(
                image=image,
                model=model,
                final_prompt=final_prompt,
                seed=resolved_seed,
                used_fallback=tried_fallback,
                rate_limited_primary=rate_limited_primary,
            )
        except Exception as exc:
            if index == 0 and _is_rate_limit(exc):
                rate_limited_primary = True
            errors.append(_friendly_error(exc, model))
            if index < len(models) - 1:
                continue

    if tried_fallback and rate_limited_primary:
        message = (
            "Both models are temporarily unavailable. Please wait and try again."
        )
    elif tried_fallback:
        message = (
            "Both models are temporarily unavailable. Please wait and try again.\n\n"
            + "\n".join(errors)
        )
    else:
        message = errors[0] if errors else "Unknown generation error."

    return GenerationError(
        message=message,
        tried_fallback=tried_fallback,
        rate_limited=rate_limited_primary,
    )
