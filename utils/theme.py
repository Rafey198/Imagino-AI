"""Dark neon theme CSS for Imagino AI."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ─────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0a12 0%, #12101f 35%, #0d1528 70%, #0a0a12 100%);
    background-attachment: fixed;
    color: #e8e8f0;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* ── Typography ───────────────────────────────────────── */
h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.02em;
}

/* ── Glass cards ──────────────────────────────────────── */
.glass-card {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
}

/* ── Header ───────────────────────────────────────────── */
.app-header {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
    margin-bottom: 0.5rem;
}

.app-logo {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa 0%, #60a5fa 40%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 24px rgba(167, 139, 250, 0.45));
    margin-bottom: 0.25rem;
    letter-spacing: -0.03em;
}

.app-tagline {
    font-size: 1.15rem;
    color: rgba(232, 232, 240, 0.65);
    font-weight: 300;
    margin-top: 0.5rem;
}

/* ── Section labels ───────────────────────────────────── */
.section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #a78bfa;
    margin-bottom: 0.75rem;
}

/* ── Sidebar ──────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0e0e18 0%, #14122a 100%);
    border-right: 1px solid rgba(167, 139, 250, 0.12);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

.sidebar-logo {
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.sidebar-subtitle {
    font-size: 0.85rem;
    color: rgba(232, 232, 240, 0.5);
    margin-bottom: 1.5rem;
}

.sidebar-section {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
}

.sidebar-section h4 {
    font-size: 0.8rem;
    font-weight: 600;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0 0 0.6rem 0;
}

.sidebar-section p, .sidebar-section li {
    font-size: 0.85rem;
    color: rgba(232, 232, 240, 0.7);
    line-height: 1.55;
    margin: 0;
}

.sidebar-section ul {
    padding-left: 1.1rem;
    margin: 0;
}

.status-ok {
    color: #34d399;
    font-weight: 500;
}

.status-error {
    color: #f87171;
    font-weight: 500;
}

/* ── Inputs ───────────────────────────────────────────── */
.stTextArea textarea, .stTextInput input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'Outfit', sans-serif !important;
}

.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(167, 139, 250, 0.5) !important;
    box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.15) !important;
}

/* Selectbox & sliders */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
}

div[data-baseweb="slider"] > div > div {
    background: rgba(167, 139, 250, 0.25) !important;
}

div[data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
    box-shadow: 0 0 12px rgba(167, 139, 250, 0.5) !important;
}

/* ── Generate button ──────────────────────────────────── */
div.stButton > button[kind="primary"],
div.stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, #7c3aed 0%, #3b82f6 50%, #06b6d4 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 24px rgba(124, 58, 237, 0.4),
                0 0 40px rgba(59, 130, 246, 0.15) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    width: 100%;
}

div.stButton > button[kind="primary"]:hover,
div.stButton > button[data-testid="stBaseButton-primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 32px rgba(124, 58, 237, 0.55),
                0 0 50px rgba(59, 130, 246, 0.25) !important;
}

div.stButton > button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
}

/* ── Output panel ─────────────────────────────────────── */
.output-panel {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(167, 139, 250, 0.15);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: 0 0 40px rgba(167, 139, 250, 0.08);
}

.meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.75rem;
    margin-top: 1rem;
}

.meta-item {
    background: rgba(255, 255, 255, 0.04);
    border-radius: 10px;
    padding: 0.65rem 0.85rem;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.meta-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(167, 139, 250, 0.8);
    margin-bottom: 0.2rem;
}

.meta-value {
    font-size: 0.85rem;
    color: #e8e8f0;
    font-family: 'JetBrains Mono', monospace;
    word-break: break-word;
}

/* ── History cards ────────────────────────────────────── */
.history-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    padding: 0.85rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s ease;
}

.history-card:hover {
    border-color: rgba(167, 139, 250, 0.25);
}

.history-prompt {
    font-size: 0.82rem;
    color: rgba(232, 232, 240, 0.75);
    margin-top: 0.4rem;
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
}

.history-meta {
    font-size: 0.72rem;
    color: rgba(232, 232, 240, 0.45);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 0.35rem;
}

/* ── Alerts ───────────────────────────────────────────── */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* ── Image border glow ────────────────────────────────── */
.result-image-wrap img {
    border-radius: 16px;
    border: 1px solid rgba(167, 139, 250, 0.2);
    box-shadow: 0 0 60px rgba(124, 58, 237, 0.15);
}

/* ── Download button ──────────────────────────────────── */
.stDownloadButton > button {
    background: rgba(52, 211, 153, 0.12) !important;
    border: 1px solid rgba(52, 211, 153, 0.35) !important;
    color: #34d399 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.stDownloadButton > button:hover {
    background: rgba(52, 211, 153, 0.22) !important;
    box-shadow: 0 0 20px rgba(52, 211, 153, 0.2) !important;
}

/* ── Spinner ──────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #a78bfa !important;
}
</style>
"""
