# Imagino AI

**Turn words into stunning AI-generated images.**

A polished Streamlit app for AI image generation powered by the Hugging Face Inference API.

**GitHub:** [https://github.com/Rafey198/Imagino-AI](https://github.com/Rafey198/Imagino-AI)

---

## Features

- Text-to-image with **FLUX.1-schnell** (primary) and **SDXL** (automatic fallback)
- 10 style presets that enhance your prompt
- 5 aspect ratios with mapped resolutions
- Adjustable inference steps, guidance scale, and seed
- Session history gallery with thumbnails
- Dark neon UI with glassmorphism design
- Works locally and on Streamlit Cloud

---

## Local setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or on Windows if `pip` is not on PATH:

```bash
python -m pip install -r requirements.txt
```

### 2. Create a Hugging Face token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Create a token with **Inference Providers** permission
3. Copy the token (starts with `hf_`)

### 3. Create `.env` file

```bash
copy .env.example .env
```

Edit `.env`:

```
HF_TOKEN=your_token_here
```

> **Never commit `.env`** — it is listed in `.gitignore`.

### 4. Run the app

```bash
streamlit run streamlit_app.py
```

Opens at **http://localhost:8501**.

---

## Token configuration

The app reads `HF_TOKEN` in this order:

1. **Streamlit secrets** (`st.secrets`) — used on Streamlit Cloud
2. **Environment variable** — from `.env` via `python-dotenv` for local dev

---

## Streamlit Cloud deployment

| Setting | Value |
|---------|-------|
| **Repository** | `Rafey198/Imagino-AI` |
| **Branch** | `main` |
| **Main file path** | `streamlit_app.py` |

### Add secrets in Streamlit Cloud

1. Open your app on [share.streamlit.io](https://share.streamlit.io)
2. Go to **Settings → Secrets**
3. Add:

```toml
HF_TOKEN = "your_huggingface_token_here"
```

4. Save and reboot the app

---

## Models

| Role | Model |
|------|-------|
| Primary | `black-forest-labs/FLUX.1-schnell` |
| Fallback | `stabilityai/stable-diffusion-xl-base-1.0` |

If the primary model fails, rate-limits (HTTP 429), or times out, the app automatically tries the fallback.

---

## Project structure

```
Imagino-AI/
├── streamlit_app.py      # Main app entry point
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── utils/
    ├── image_generator.py
    └── theme.py
```

---

## Troubleshooting

### Missing HF_TOKEN

**Fix:** Add `HF_TOKEN` to `.env` locally, or to Streamlit secrets when deployed. Restart the app.

### HTTP 429 — Rate limit

The app shows *"Rate limit reached on this model. Trying fallback model..."* and switches to SDXL. If both fail, wait a few minutes and try again.

### Model warming up (503)

Wait 30–60 seconds and click **Generate** again.

### Network / timeout

Check your connection. Generation can take 15–60 seconds.

---

## License

For personal and educational use. Respect the licenses of the underlying Hugging Face models.
