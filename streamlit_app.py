"""Imagino AI — local Streamlit image generation app."""

from __future__ import annotations

import io
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from utils.image_generator import (
    ASPECT_RATIOS,
    PRIMARY_MODEL,
    FALLBACK_MODEL,
    STYLE_SUFFIXES,
    generate_image,
    GenerationError,
    GenerationResult,
)
from utils.theme import CUSTOM_CSS

load_dotenv()

# Placeholder values that must not be treated as real tokens
_INVALID_TOKEN_VALUES = {"", "your_huggingface_token_here", "your_token_here"}


def get_hf_token() -> str:
    """Return HF token from Streamlit secrets first, then environment."""
    token = ""
    try:
        token = st.secrets["HF_TOKEN"]
    except Exception:
        pass
    if not token:
        token = os.environ.get("HF_TOKEN", "")
    token = str(token).strip().strip('"').strip("'")
    if token in _INVALID_TOKEN_VALUES:
        return ""
    return token


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Imagino AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history: list[dict] = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


def clear_history() -> None:
    st.session_state.history = []
    st.session_state.last_result = None


def add_to_history(entry: dict) -> None:
    st.session_state.history.insert(0, entry)


def get_token_status() -> tuple[bool, str]:
    token = get_hf_token()
    if token:
        return True, "Connected"
    return False, "Missing or invalid"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">✨ Imagino AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-subtitle">Turn words into stunning AI-generated images.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-section">
            <h4>How to use</h4>
            <p>1. Enter your prompt<br>
            2. Pick a style &amp; aspect ratio<br>
            3. Adjust settings if needed<br>
            4. Click <strong>Generate Image</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-section">
            <h4>Prompt tips</h4>
            <ul>
                <li>Be specific about subject, lighting, and mood</li>
                <li>Use style presets to enhance your prompt</li>
                <li>Add details: colors, camera angle, atmosphere</li>
                <li>Use negative prompts to exclude unwanted elements</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="sidebar-section">
            <h4>Models</h4>
            <p><strong>Primary:</strong><br>{PRIMARY_MODEL}</p>
            <p style="margin-top:0.5rem"><strong>Fallback:</strong><br>{FALLBACK_MODEL}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    token_ok, token_label = get_token_status()
    status_class = "status-ok" if token_ok else "status-error"
    st.markdown(
        f"""
        <div class="sidebar-section">
            <h4>HF Token</h4>
            <p class="{status_class}">{'✓ ' if token_ok else '✗ '}{token_label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Clear History", use_container_width=True):
        clear_history()
        st.rerun()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="app-header">
        <div class="app-logo">Imagino AI</div>
        <div class="app-tagline">Turn words into stunning AI-generated images.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Main layout ─────────────────────────────────────────────────────────────────
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.markdown('<div class="section-label">Prompt</div>', unsafe_allow_html=True)
    prompt = st.text_area(
        "Main prompt",
        placeholder="Describe the image you want to create…",
        height=120,
        label_visibility="collapsed",
    )

    st.markdown('<div class="section-label">Negative Prompt</div>', unsafe_allow_html=True)
    negative_prompt = st.text_area(
        "Negative prompt",
        placeholder="What to avoid: blurry, low quality, watermark…",
        height=80,
        label_visibility="collapsed",
    )

    settings_col1, settings_col2 = st.columns(2)

    with settings_col1:
        style = st.selectbox("Style Preset", list(STYLE_SUFFIXES.keys()))
        aspect_ratio = st.selectbox("Aspect Ratio", list(ASPECT_RATIOS.keys()))

    with settings_col2:
        num_steps = st.slider("Inference Steps", min_value=1, max_value=50, value=4)
        guidance_scale = st.slider("Guidance Scale", min_value=0.0, max_value=20.0, value=7.5, step=0.5)

    seed = st.number_input("Seed (-1 for random)", min_value=-1, value=-1, step=1)

    generate_clicked = st.button("✨ Generate Image", type="primary", use_container_width=True)

with col_output:
    st.markdown('<div class="section-label">Result</div>', unsafe_allow_html=True)

    if generate_clicked:
        if not prompt or not prompt.strip():
            st.error("Please enter a prompt before generating.")
        else:
            token = get_hf_token()
            if not token:
                st.error(
                    "HF_TOKEN is missing. Add it to `.env` locally or Streamlit secrets "
                    "(Settings → Secrets) and restart the app."
                )
            else:
                with st.spinner("Generating your image… this may take a moment."):
                    result = generate_image(
                        token=token,
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        style=style,
                        aspect_ratio=aspect_ratio,
                        num_inference_steps=num_steps,
                        guidance_scale=guidance_scale,
                        seed=seed,
                    )

                if isinstance(result, GenerationError):
                    if result.rate_limited and result.tried_fallback:
                        st.warning(
                            "Rate limit reached on this model. Trying fallback model…"
                        )
                    st.error(result.message)
                else:
                    if result.rate_limited_primary:
                        st.warning(
                            "Rate limit reached on this model. Trying fallback model…"
                        )
                    st.session_state.last_result = {
                        "image": result.image,
                        "model": result.model,
                        "final_prompt": result.final_prompt,
                        "style": style,
                        "aspect_ratio": aspect_ratio,
                        "seed": result.seed,
                        "steps": num_steps,
                        "guidance_scale": guidance_scale,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "user_prompt": prompt.strip(),
                    }
                    add_to_history(st.session_state.last_result.copy())

    # Display latest result
    if st.session_state.last_result:
        data = st.session_state.last_result
        st.markdown('<div class="output-panel">', unsafe_allow_html=True)
        st.markdown('<div class="result-image-wrap">', unsafe_allow_html=True)
        st.image(data["image"], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        buf = io.BytesIO()
        data["image"].save(buf, format="PNG")
        st.download_button(
            label="⬇ Download PNG",
            data=buf.getvalue(),
            file_name=f"imagino_{data['seed']}.png",
            mime="image/png",
            use_container_width=True,
        )

        st.markdown(
            f"""
            <div class="meta-grid">
                <div class="meta-item">
                    <div class="meta-label">Model</div>
                    <div class="meta-value">{data['model'].split('/')[-1]}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Style</div>
                    <div class="meta-value">{data['style']}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Aspect Ratio</div>
                    <div class="meta-value">{data['aspect_ratio']}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Seed</div>
                    <div class="meta-value">{data['seed']}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Steps</div>
                    <div class="meta-value">{data['steps']}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-label">Guidance</div>
                    <div class="meta-value">{data['guidance_scale']}</div>
                </div>
            </div>
            <div class="meta-item" style="margin-top:0.75rem">
                <div class="meta-label">Final Prompt</div>
                <div class="meta-value">{data['final_prompt']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div class="output-panel" style="text-align:center;padding:3rem 1.5rem">
                <p style="color:rgba(232,232,240,0.4);font-size:1.1rem">
                    Your generated image will appear here
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Session history ─────────────────────────────────────────────────────────────
if st.session_state.history:
    st.markdown("---")
    st.markdown('<div class="section-label">Session History</div>', unsafe_allow_html=True)

    hist_cols = st.columns(min(len(st.session_state.history), 4))
    for i, entry in enumerate(st.session_state.history[:8]):
        with hist_cols[i % len(hist_cols)]:
            st.markdown('<div class="history-card">', unsafe_allow_html=True)
            st.image(entry["image"], use_container_width=True)
            st.markdown(
                f"""
                <div class="history-prompt">{entry['user_prompt']}</div>
                <div class="history-meta">
                    {entry['timestamp']} · {entry['model'].split('/')[-1]}
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("View", key=f"view_{i}", use_container_width=True):
                st.session_state.last_result = entry
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
