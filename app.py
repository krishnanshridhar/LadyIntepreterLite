import streamlit as st
from datetime import datetime
import os

st.set_page_config(
    page_title="She Said What? v2",
    page_icon="💑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
for k, v in {
    "mode": "comedy",
    "history": [],
    "phrase_result": None,
    "phrase_current": None,
    "emoji_quick": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

mode = st.session_state.mode

# ══════════════════════════════════════════════════════════════════════════════
# CSS — exhaustive targeting of every Streamlit element for full readability
# ══════════════════════════════════════════════════════════════════════════════
COMEDY_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@400;600;700;800&display=swap');

/* ── RESET & BASE ── */
html, body, [class*="css"], .stApp { font-family: 'Nunito', sans-serif !important; }
h1, h2, h3, .stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Bangers', cursive !important;
    letter-spacing: 2px !important;
    color: #111111 !important;
}

/* ── APP BACKGROUND ── */
.stApp, .main, .block-container {
    background-color: #FFFFFF !important;
    color: #111111 !important;
}
.block-container { padding-top: 2rem !important; max-width: 900px; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] .block-container {
    background-color: #FFE600 !important;
    border-right: 4px solid #111111 !important;
}
section[data-testid="stSidebar"] * { color: #111111 !important; }
section[data-testid="stSidebar"] h2 { font-family: 'Bangers', cursive !important; font-size: 1.4rem !important; }
section[data-testid="stSidebar"] hr { border-color: #111111 !important; border-width: 2px !important; }

/* ── ALL WIDGET LABELS (the big fix) ── */
label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stSlider label,
.stMultiSelect label,
.stCheckbox label,
.stRadio label,
.stDateInput label,
div[class*="stSelectbox"] label,
div[class*="stTextInput"] label,
div[class*="stTextArea"] label,
div[class*="stSlider"] label,
div[class*="stMultiSelect"] label,
div[class*="stRadio"] label,
div[class*="stCheckbox"] label,
.stMarkdown p,
.stMarkdown li,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
p, span, li, td, th {
    color: #111111 !important;
}
small, .stCaption, [data-testid="stCaptionContainer"] p { color: #444444 !important; font-size: 0.85rem !important; }

/* ── TEXT INPUTS & TEXTAREAS ── */
.stTextInput input,
.stTextArea textarea,
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #111111 !important;
    border: 3px solid #111111 !important;
    border-radius: 4px !important;
    box-shadow: 3px 3px 0 #111111 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.5rem 0.75rem !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #C41230 !important;
    box-shadow: 3px 3px 0 #C41230 !important;
    outline: none !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: #666666 !important; opacity: 1 !important; }

/* ── SELECT BOXES ── */
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div {
    background-color: #FFFFFF !important;
    border: 3px solid #111111 !important;
    border-radius: 4px !important;
    box-shadow: 3px 3px 0 #111111 !important;
    color: #111111 !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div { color: #111111 !important; }
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[data-baseweb="menu"] { background-color: #FFFFFF !important; border: 3px solid #111111 !important; }
div[data-baseweb="option"] { background-color: #FFFFFF !important; color: #111111 !important; }
div[data-baseweb="option"]:hover { background-color: #FFE600 !important; color: #111111 !important; }

/* ── MULTISELECT ── */
div[data-baseweb="tag"] {
    background-color: #C41230 !important;
    border: 2px solid #111111 !important;
    border-radius: 3px !important;
}
div[data-baseweb="tag"] span { color: #FFFFFF !important; font-weight: 700 !important; }

/* ── SLIDERS ── */
[data-testid="stSlider"] [data-testid="stWidgetLabel"] p { color: #111111 !important; font-weight: 700 !important; }
[data-testid="stSlider"] p { color: #111111 !important; }
[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p { color: #555555 !important; }
div[data-testid="stSlider"] > div > div > div > div { background-color: #111111 !important; }
div[data-testid="stSlider"] > div > div > div > div > div { background-color: #C41230 !important; }
[data-testid="stThumbValue"], [data-testid="stTickBarMin"], [data-testid="stTickBarMax"] {
    color: #111111 !important; font-weight: 700 !important;
}

/* ── CHECKBOXES & RADIOS ── */
.stCheckbox > label > div > p { color: #111111 !important; font-weight: 600 !important; }
.stRadio > div > label > div > p { color: #111111 !important; font-weight: 600 !important; }
.stRadio > div { gap: 6px !important; }

/* ── BUTTONS ── */
.stButton > button {
    background-color: #C41230 !important;
    color: #FFFFFF !important;
    border: 3px solid #111111 !important;
    border-radius: 4px !important;
    font-family: 'Bangers', cursive !important;
    font-size: 1.1rem !important;
    letter-spacing: 1.5px !important;
    box-shadow: 4px 4px 0 #111111 !important;
    transition: transform 0.08s, box-shadow 0.08s !important;
    padding: 0.5rem 1.5rem !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translate(-2px, -2px) !important;
    box-shadow: 6px 6px 0 #111111 !important;
    background-color: #A10E28 !important;
}
.stButton > button:active {
    transform: translate(2px, 2px) !important;
    box-shadow: 2px 2px 0 #111111 !important;
}

/* ── EXPANDERS ── */
[data-testid="stExpander"],
.streamlit-expanderHeader,
[data-testid="stExpanderDetails"] {
    background-color: #FFFFFF !important;
    border: 2px solid #111111 !important;
    border-radius: 4px !important;
}
.streamlit-expanderHeader p,
[data-testid="stExpanderToggleIcon"],
[data-testid="stExpander"] summary p { color: #111111 !important; font-weight: 700 !important; }

/* ── ALERTS / INFO BOXES ── */
.stAlert, [data-testid="stAlert"] {
    background-color: #FFF9C4 !important;
    border: 2px solid #111111 !important;
    border-radius: 4px !important;
    box-shadow: 3px 3px 0 #111111 !important;
}
.stAlert p, .stAlert div, [data-testid="stAlert"] p { color: #111111 !important; font-weight: 600 !important; }

/* ── METRICS ── */
[data-testid="stMetric"] { background: #FFF9C4 !important; border: 3px solid #111111 !important; border-radius: 4px !important; padding: 1rem !important; box-shadow: 4px 4px 0 #111111 !important; }
[data-testid="stMetricLabel"] p { color: #111111 !important; font-weight: 700 !important; }
[data-testid="stMetricValue"] { color: #C41230 !important; font-family: 'Bangers', cursive !important; font-size: 2rem !important; }

/* ── SPINNER ── */
[data-testid="stSpinner"] p, .stSpinner p { color: #111111 !important; font-weight: 700 !important; }

/* ── DIVIDER ── */
hr { border: 2px solid #111111 !important; }

/* ── CUSTOM RESULT BLOCK ── */
.result-block {
    background: #FFFFFF;
    border: 3px solid #111111;
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-top: 1.5rem;
    box-shadow: 6px 6px 0 #111111;
    position: relative;
}
.result-block::before {
    content: "★ DECODED ★";
    font-family: 'Bangers', cursive;
    font-size: 0.82rem;
    letter-spacing: 2px;
    background: #FFE600;
    border: 2px solid #111111;
    padding: 3px 14px;
    position: absolute;
    top: -14px;
    left: 18px;
}
.result-block p, .result-block li, .result-block td { color: #111111 !important; font-size: 1rem !important; line-height: 1.8 !important; }
.result-block h3 { font-family: 'Bangers', cursive !important; color: #C41230 !important; font-size: 1.25rem !important; letter-spacing: 1px !important; margin-top: 1.2rem !important; }
.result-block strong { color: #111111 !important; font-weight: 800 !important; }
.result-block ul, .result-block ol { padding-left: 1.5rem !important; }
.result-block code { background: #FFF9C4 !important; border: 1px solid #111111 !important; padding: 1px 6px !important; border-radius: 2px !important; }

/* ── MODE BADGE ── */
.mode-badge {
    display: inline-block;
    background: #C41230;
    color: #FFFFFF;
    font-family: 'Bangers', cursive;
    font-size: 0.9rem;
    letter-spacing: 2px;
    padding: 4px 16px;
    border: 3px solid #111111;
    box-shadow: 3px 3px 0 #111111;
    margin-bottom: 1rem;
}

/* ── DIVIDERS ── */
.fdiv {
    height: 4px;
    background-image: repeating-linear-gradient(90deg,#111111 0,#111111 16px,#FFE600 16px,#FFE600 20px);
    margin: 1.5rem 0;
    border-radius: 2px;
}

/* ── MOBILE ── */
@media (max-width: 768px) {
    div[data-testid="column"] { width:100%!important; flex:1 1 100%!important; min-width:100%!important; }
    h1 { font-size: 1.9rem !important; }
    .block-container { padding: 1rem 0.7rem !important; }
    .result-block { padding: 1.2rem 1.2rem !important; }
}
"""

SERIOUS_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Nunito:wght@400;500;600&display=swap');

/* ── RESET & BASE ── */
html, body, [class*="css"], .stApp { font-family: 'Nunito', sans-serif !important; }
h1, h2, h3, .stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: #1C1208 !important;
    font-weight: 700 !important;
}

/* ── APP BACKGROUND ── */
.stApp, .main { background-color: #FAF6F0 !important; color: #1C1208 !important; }
.block-container { background-color: #FAF6F0 !important; padding-top: 2rem !important; max-width: 900px; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] .block-container {
    background-color: #EDE8DF !important;
    border-right: 1px solid #C8BAA8 !important;
}
section[data-testid="stSidebar"] * { color: #3A2A1A !important; }
section[data-testid="stSidebar"] h2 { font-family: 'Playfair Display', serif !important; font-size: 1.2rem !important; color: #8B5E3C !important; }
section[data-testid="stSidebar"] hr { border-color: #C8BAA8 !important; }

/* ── ALL WIDGET LABELS ── */
label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stTextInput label, .stTextArea label, .stSelectbox label,
.stSlider label, .stMultiSelect label,
.stCheckbox label, .stRadio label, .stDateInput label,
div[class*="stSelectbox"] label, div[class*="stTextInput"] label,
div[class*="stTextArea"] label, div[class*="stSlider"] label,
div[class*="stMultiSelect"] label, div[class*="stRadio"] label,
div[class*="stCheckbox"] label,
.stMarkdown p, .stMarkdown li,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
p, span, li, td, th {
    color: #1C1208 !important;
}
small, .stCaption, [data-testid="stCaptionContainer"] p { color: #7A6A58 !important; font-size: 0.85rem !important; }
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: #4A3A2A !important; }

/* ── TEXT INPUTS ── */
.stTextInput input, .stTextArea textarea,
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #1C1208 !important;
    border: 1.5px solid #C8BAA8 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.55rem 0.85rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #8B5E3C !important;
    box-shadow: 0 0 0 3px rgba(139,94,60,0.12) !important;
    outline: none !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #7A6558 !important; opacity: 1 !important; }

/* ── SELECT BOXES ── */
div[data-baseweb="select"] > div, div[data-baseweb="select"] > div > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid #C8BAA8 !important;
    border-radius: 8px !important;
    color: #1C1208 !important;
    box-shadow: none !important;
}
div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: #1C1208 !important; }
div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #C8BAA8 !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 20px rgba(28,18,8,0.12) !important;
}
div[data-baseweb="option"] { background-color: #FFFFFF !important; color: #1C1208 !important; }
div[data-baseweb="option"]:hover { background-color: #F3EDE3 !important; }

/* ── MULTISELECT ── */
div[data-baseweb="tag"] {
    background-color: rgba(139,94,60,0.15) !important;
    border: 1px solid rgba(139,94,60,0.4) !important;
    border-radius: 20px !important;
}
div[data-baseweb="tag"] span { color: #5C3A1E !important; font-weight: 600 !important; }

/* ── SLIDERS ── */
[data-testid="stSlider"] [data-testid="stWidgetLabel"] p { color: #1C1208 !important; font-weight: 600 !important; }
[data-testid="stSlider"] p { color: #1C1208 !important; }
[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p { color: #7A6A58 !important; }
div[data-testid="stSlider"] > div > div > div > div { background-color: #D4C0A8 !important; }
div[data-testid="stSlider"] > div > div > div > div > div { background-color: #8B5E3C !important; }
[data-testid="stThumbValue"], [data-testid="stTickBarMin"], [data-testid="stTickBarMax"] { color: #3A2A1A !important; }

/* ── CHECKBOXES & RADIOS ── */
.stCheckbox > label > div > p { color: #1C1208 !important; font-weight: 500 !important; }
.stRadio > div > label > div > p { color: #1C1208 !important; font-weight: 500 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background-color: #8B5E3C !important;
    color: #FAF6F0 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 2px 8px rgba(139,94,60,0.25) !important;
    transition: background-color 0.2s, transform 0.15s, box-shadow 0.15s !important;
    padding: 0.55rem 1.5rem !important;
    width: 100% !important;
}
.stButton > button:hover {
    background-color: #6B4428 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 5px 16px rgba(139,94,60,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── EXPANDERS ── */
[data-testid="stExpander"], .streamlit-expanderHeader {
    background-color: #FFFFFF !important;
    border: 1px solid #D4C4B0 !important;
    border-radius: 8px !important;
}
.streamlit-expanderHeader p,
[data-testid="stExpander"] summary p { color: #3A2A1A !important; font-weight: 600 !important; }

/* ── ALERTS / INFO BOXES ── */
.stAlert, [data-testid="stAlert"] {
    background-color: #F3EDE3 !important;
    border: 1px solid #C8BAA8 !important;
    border-left: 4px solid #8B5E3C !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}
.stAlert p, .stAlert div, [data-testid="stAlert"] p { color: #3A2A1A !important; font-weight: 500 !important; }

/* ── METRICS ── */
[data-testid="stMetric"] { background: #FFFFFF !important; border: 1px solid #D4C4B0 !important; border-radius: 10px !important; padding: 1rem !important; box-shadow: 0 2px 10px rgba(28,18,8,0.06) !important; }
[data-testid="stMetricLabel"] p { color: #7A6A58 !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: #8B5E3C !important; font-size: 2rem !important; font-weight: 700 !important; }

/* ── SPINNER ── */
[data-testid="stSpinner"] p, .stSpinner p { color: #7A6A58 !important; }

/* ── DIVIDER ── */
hr { border: none !important; border-top: 1px solid #D4C4B0 !important; }

/* ── CUSTOM RESULT BLOCK ── */
.result-block {
    background: #FFFFFF;
    border: 1px solid #D4C4B0;
    border-left: 5px solid #8B5E3C;
    border-radius: 10px;
    padding: 2rem 2.2rem;
    margin-top: 1.5rem;
    box-shadow: 0 3px 16px rgba(28,18,8,0.07);
    line-height: 1.9;
}
.result-block p, .result-block li, .result-block td { color: #1C1208 !important; font-size: 0.97rem !important; line-height: 1.85 !important; }
.result-block h3 { font-family: 'Playfair Display', serif !important; color: #8B5E3C !important; font-size: 1.1rem !important; font-weight: 700 !important; margin-top: 1.3rem !important; border-bottom: 1px solid #EDE8DF; padding-bottom: 4px; }
.result-block strong { color: #3A2A1A !important; font-weight: 700 !important; }
.result-block ul, .result-block ol { padding-left: 1.5rem !important; }
.result-block code { background: #F3EDE3 !important; color: #5C3A1E !important; padding: 1px 6px !important; border-radius: 4px !important; }
.result-block blockquote { border-left: 3px solid #8B5E3C !important; padding-left: 1rem !important; color: #5C4A38 !important; font-style: italic !important; }

/* ── MODE BADGE ── */
.mode-badge {
    display: inline-block;
    background: #8B5E3C;
    color: #FAF6F0;
    font-family: 'Playfair Display', serif;
    font-size: 0.78rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 3px;
    margin-bottom: 0.8rem;
}

/* ── DIVIDERS ── */
.fdiv { height: 1px; background: linear-gradient(90deg, transparent, #C8BAA8 40%, #C8BAA8 60%, transparent); margin: 1.5rem 0; }

/* ── MOBILE ── */
@media (max-width: 768px) {
    div[data-testid="column"] { width:100%!important; flex:1 1 100%!important; min-width:100%!important; }
    h1 { font-size: 1.5rem !important; }
    .block-container { padding: 1rem 0.7rem !important; }
    .result-block { padding: 1.2rem 1.4rem !important; border-left-width: 4px !important; }
}
"""

st.markdown(f"<style>{COMEDY_CSS if mode == 'comedy' else SERIOUS_CSS}</style>", unsafe_allow_html=True)

# ─── API KEY CHECK ────────────────────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    st.error(
        "**ANTHROPIC_API_KEY not set.**\n\n"
        "Run: `ANTHROPIC_API_KEY=your_key streamlit run app.py`\n\n"
        "On Streamlit Cloud: Manage app → Settings → Secrets."
    )
    st.stop()

import anthropic
client = anthropic.Anthropic(api_key=api_key)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def ask_claude(system_prompt: str, user_msg: str, max_tokens: int = 1200) -> str:
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_msg}]
        )
        return resp.content[0].text
    except anthropic.AuthenticationError:
        return "❌ **Authentication error** — check your API key at console.anthropic.com"
    except anthropic.RateLimitError:
        return "❌ **Rate limit reached** — wait a moment then try again."
    except anthropic.APIStatusError as e:
        return f"❌ **API error ({e.status_code})** — {e.message}"
    except Exception as e:
        return f"❌ **Unexpected error** — {str(e)}"

def show_result(result: str):
    st.markdown('<div class="result-block">', unsafe_allow_html=True)
    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

def save_history(feature: str, input_text: str, result: str):
    snippet = input_text[:100] + ("..." if len(input_text) > 100 else "")
    st.session_state.history.insert(0, {
        "feature": feature, "input": snippet, "result": result,
        "time": datetime.now().strftime("%d %b %H:%M"), "mode": mode,
    })
    if len(st.session_state.history) > 20:
        st.session_state.history = st.session_state.history[:20]

def validate(text: str, label: str = "This field") -> bool:
    if not text.strip():
        st.warning(f"⚠️ {label} can't be empty.")
        return False
    return True

def divider():
    st.markdown('<div class="fdiv"></div>', unsafe_allow_html=True)

def mode_badge(label: str):
    st.markdown(f'<div class="mode-badge">{label}</div>', unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    if mode == "comedy":
        st.markdown("<h2>💥 SHE SAID WHAT?!</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.82rem; font-weight:700;'>Survival guide to female communication</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h2>She Said What?</h2>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.82rem;'>Thoughtful relationship tools</p>", unsafe_allow_html=True)

    st.divider()

    # ── MODE TOGGLE ──────────────────────────────────────────────────────────
    st.markdown("**Switch mode**")
    cola, colb = st.columns(2)
    with cola:
        if st.button("😂 Comedy", use_container_width=True):
            st.session_state.mode = "comedy"
            st.session_state.phrase_result = None
            st.rerun()
    with colb:
        if st.button("🧠 Serious", use_container_width=True):
            st.session_state.mode = "serious"
            st.session_state.phrase_result = None
            st.rerun()

    if mode == "comedy":
        st.caption("For laughs. May cause uncomfortable recognition.")
    else:
        st.caption("For moments that actually matter.")

    st.divider()

    # ── PERSONALISE ──────────────────────────────────────────────────────────
    st.markdown("**Personalise**")
    her_name = st.text_input("Her name / nickname", value="her", help="Used to personalise all responses")
    your_name = st.text_input("Your name", value="me")
    rel_type  = st.selectbox("Relationship", ["Wife", "Girlfriend", "Fiancée", "Partner"])
    years     = st.slider("Years together", 0, 30, 2)
    st.divider()

    # ── NAV ──────────────────────────────────────────────────────────────────
    st.markdown("**Features**")
    if mode == "comedy":
        page = st.radio("", [
            "💬 What She Really Said",
            "📖 The Phrase Bible",
            "🚨 Danger Meter",
            "🔢 Emoji Translator",
            "😶 Silence Decoder",
            "🕑 History",
        ], label_visibility="collapsed")
        st.divider()
        st.caption("For entertainment only. Results may cause recognition, laughter, or mild panic.")
    else:
        page = st.radio("", [
            "🙏 Apology Workshop",
            "⚖️ Argument Referee",
            "🎁 Gift Advisor",
            "📅 Date Planner",
            "🌡️ Relationship Check-in",
            "🕑 History",
        ], label_visibility="collapsed")
        st.divider()
        st.caption("Best for genuine moments — not for over-analysing normal conversation.")

rel_label = her_name.strip() if her_name.strip() not in ("", "her") else rel_type.lower()


# ════════════════════════════════════════════════════════════════
#  C O M E D Y   M O D E
# ════════════════════════════════════════════════════════════════
if mode == "comedy":

    # ── 💬 WHAT SHE REALLY SAID ─────────────────────────────────────────────
    if page == "💬 What She Really Said":
        st.markdown("<h1>💬 WHAT SHE REALLY SAID</h1>", unsafe_allow_html=True)
        mode_badge("⚡ COMEDY MODE")
        st.caption("She said one thing. She meant another. Let's find out what.")

        input_type = st.radio("Input type:", ["Single message", "Full conversation"], horizontal=True)
        if input_type == "Single message":
            msg     = st.text_area(f"What did {rel_label} say?", height=100,
                        placeholder='"Fine." / "Do whatever you want." / "I\'m not mad."')
            context = st.text_input("Context (optional):", placeholder="e.g. After I said I was going to watch cricket")
        else:
            msg     = st.text_area("Paste the conversation:", height=210,
                        placeholder="Paste WhatsApp / iMessage chat here...")
            context = st.text_input("Context (optional):", placeholder="e.g. This was about weekend plans")

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            go = st.button("💥 DECODE IT", use_container_width=True)

        if go:
            if not validate(msg, "The message"): st.stop()
            with st.spinner("Translating from Female to Human..."):
                sp = f"""You are a hilariously accurate relationship translator. {your_name} is trying to understand their {rel_type.lower()} ({rel_label}), together {years} year(s).

Be FUNNY but also uncomfortably accurate — the best comedy comes from recognition.

Use these exact section headings with markdown:

### 💬 WHAT SHE SAID
Quote the key phrase(s)

### 🤔 WHAT SHE MEANT
The real message. Specific, funny, no sugar-coating.

### 🌡️ THREAT LEVEL
One of: 🟢 Stand Down / 🟡 Proceed With Caution / 🔴 MAYDAY / ☢️ ABANDON SHIP
One-line reason. Make it funny.

### 🎯 YOUR MISSION
3 specific actions. Numbered. Funny but actually useful.

### 💀 DO NOT
2 things that will make this exponentially worse. Voice of experience.

### 🏆 THE MAGIC WORDS
One sentence they can say RIGHT NOW.

### 🔮 PROPHECY
Right thing vs. wrong thing outcome. Brief, funny, painfully accurate."""
                prompt = f"Message: {msg}" + (f"\nContext: {context}" if context.strip() else "")
                result = ask_claude(sp, prompt, 1400)
                save_history("💬 What She Really Said", msg, result)
            show_result(result)

    # ── 📖 THE PHRASE BIBLE ──────────────────────────────────────────────────
    elif page == "📖 The Phrase Bible":
        st.markdown("<h1>📖 THE PHRASE BIBLE</h1>", unsafe_allow_html=True)
        mode_badge("⚡ COMEDY MODE")
        st.caption("Sacred texts. Study them. Know them. Fear them.")

        classics = [
            "I'm fine.",                           "Do whatever you want.",
            "Nothing's wrong.",                    "We need to talk.",
            "It's okay.",                          "If you want to.",
            "I don't care.",                       "You never listen.",
            "Must be nice.",                       "Sure, go ahead.",
            "I'm not angry, I'm disappointed.",    "Forget it.",
            "No, don't worry about it.",           "Whatever.",
            "I'm tired.",                          "It's not a big deal.",
            "You wouldn't understand.",            "I already told you.",
        ]

        st.markdown("**Click any phrase to decode it instantly:**")
        cols = st.columns(3)
        for i, phrase in enumerate(classics):
            with cols[i % 3]:
                if st.button(f'"{phrase}"', key=f"ph_{i}", use_container_width=True):
                    with st.spinner("Consulting the sacred texts..."):
                        sp = f"""You are a comedian AND relationship expert. Decode this classic {rel_type.lower()} phrase.

### 📖 THE PHRASE
Quote it in bold

### 😇 OFFICIAL MEANING
What it technically claims to mean (the lie)

### 💣 ACTUAL MEANING
What it really means — specific, funny, accurate

### ☢️ DANGER RATING
🟢 Mild / 🟡 Watch It / 🔴 Danger Zone / ☢️ Full Nuclear

### 🎓 THE PSYCHOLOGY
WHY she says this instead of what she means — one sentence, make it insightful

### 🛡️ SURVIVAL GUIDE
3 tips. Numbered. Funny but practical.

### 😂 FUN FACT
One genuinely funny observation about this phrase."""
                        result = ask_claude(sp, f'Phrase: "{phrase}"')
                        st.session_state.phrase_result  = result
                        st.session_state.phrase_current = phrase
                        save_history("📖 Phrase Bible", phrase, result)

        if st.session_state.phrase_result:
            divider()
            st.caption(f'Decoded: *"{st.session_state.phrase_current}"*')
            show_result(st.session_state.phrase_result)

        divider()
        st.markdown("**🔍 Submit your own phrase**")
        custom = st.text_input("Type any phrase:", placeholder='e.g. "Why would I be upset about that?"')
        if st.button("💥 LOOK IT UP", use_container_width=True):
            if validate(custom, "Phrase"):
                with st.spinner("Consulting the archives..."):
                    sp = f"""Decode this {rel_type.lower()} phrase: Official Meaning (the lie), Actual Meaning (the truth), Danger Rating, Psychology, Survival Guide (3 tips), Fun Fact. Be funny and accurate."""
                    result = ask_claude(sp, f'Phrase: "{custom}"')
                    st.session_state.phrase_result  = result
                    st.session_state.phrase_current = custom
                    save_history("📖 Phrase Bible", custom, result)
                    show_result(result)

    # ── 🚨 DANGER METER ──────────────────────────────────────────────────────
    elif page == "🚨 Danger Meter":
        st.markdown("<h1>🚨 DANGER METER</h1>", unsafe_allow_html=True)
        mode_badge("⚡ COMEDY MODE")
        st.caption("Describe your situation. Find out your survival probability. No judgment (okay, some judgment).")

        situation = st.text_area("Situation report:", height=130,
            placeholder="e.g. I forgot our anniversary. She said 'It's fine' and went to bed at 8pm. This morning she made tea only for herself.")

        c1, c2 = st.columns(2)
        with c1:
            how_long = st.selectbox("Duration:", [
                "Just happened", "A few hours", "Since yesterday",
                "2–3 days", "A week+", "I've completely lost track"])
        with c2:
            prev = st.selectbox("Prior offences:", [
                "First time", "Once before",
                "This is a pattern", "I'm basically always in trouble"])

        red_flags = st.multiselect("Active red flags:", [
            "She's gone quiet 🤐", "One-word text replies",
            "She's been unusually NICE 😬", "She called her mum",
            "Aggressive cleaning 🧹", "Made tea only for herself",
            "She liked your friend's photo, not yours",
            "Said 'I'm fine' more than once", "No goodnight kiss",
            "'We need to talk' received", "She's rearranging furniture",
            "She's watching sad movies alone",
        ])

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            assess = st.button("⚡ ASSESS THREAT LEVEL", use_container_width=True)

        if assess:
            if not validate(situation, "Situation"): st.stop()
            with st.spinner("Running threat assessment..."):
                sp = f"""You are a hilariously blunt relationship danger analyst for a {rel_type.lower()} situation.

### 🚨 THREAT LEVEL
State: 🟢 STAND DOWN / 🟡 ELEVATED / 🔴 HIGH ALERT / ☢️ DEFCON 1
Danger score out of 10. One-line dramatic headline.

### 🔍 FIELD ASSESSMENT
What's actually happening — specific and funny

### 📊 THREAT MULTIPLIERS
What's making this worse (patterns, red flags, duration)

### 🛠️ RECOVERY PROTOCOL
Numbered steps. Specific, practical, and funny.

### 💀 CRITICAL ERRORS
3 things that will escalate this from bad to catastrophic

### 📈 SURVIVAL PROBABILITY
A percentage with brief reasoning. Be entertainingly honest."""
                prompt = f"Situation: {situation}\nDuration: {how_long}\nPattern: {prev}\nRed flags: {', '.join(red_flags) or 'None'}"
                result = ask_claude(sp, prompt, 1300)
                save_history("🚨 Danger Meter", situation[:80], result)
            show_result(result)

    # ── 🔢 EMOJI TRANSLATOR ──────────────────────────────────────────────────
    elif page == "🔢 Emoji Translator":
        st.markdown("<h1>🔢 EMOJI TRANSLATOR</h1>", unsafe_allow_html=True)
        mode_badge("⚡ COMEDY MODE")
        st.caption("A single 🙂 from your partner contains multitudes. Let's unpack them.")

        quick_emojis = [
            ("🙂","The smile"), ("👍","Thumbs up"), ("😶","The void"), ("🙄","Eye roll"),
            ("😤","The puff"),  ("🫠","Melting"),   ("❤️‍🩹","Hurt heart"), ("🤔","Thinking"),
        ]
        st.markdown("**Quick decode — tap any:**")
        qcols = st.columns(4)
        for i, (em, label) in enumerate(quick_emojis):
            with qcols[i % 4]:
                if st.button(f"{em} {label}", key=f"eq_{i}", use_container_width=True):
                    st.session_state.emoji_quick = em

        emoji_input   = st.text_input("Emoji(s) to decode:",
                            value=st.session_state.emoji_quick,
                            placeholder="Paste emoji(s) here — e.g. 😶👍 or just 🙂")
        emoji_context = st.text_input("Context:", placeholder="e.g. After I said I'd be home late")

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            decode_em = st.button("💥 DECODE THESE EMOJIS", use_container_width=True)

        if decode_em:
            if not validate(emoji_input, "Emoji input"): st.stop()
            with st.spinner("Running emoji forensics..."):
                sp = f"""You are a relationship emoji expert. A {rel_type.lower()}'s emoji is NEVER just an emoji.

### 📱 THE EMOJI(S)
State what was sent

### 😇 CLAIMED MEANING
The naive interpretation

### 💣 ACTUAL MEANING
The real meaning in this context — specific and funny

### 🌡️ EMOTIONAL READING
Warm / Neutral / Passive-aggressive / Genuinely happy / Testing / Plotting

### ☢️ DANGER LEVEL
🟢 Safe / 🟡 Caution / 🔴 Alert

### 💬 HOW TO RESPOND
An actual suggested reply they can send right now

### 😂 THE DEEPER TRUTH
Why {rel_type.lower()}s communicate via emoji instead of just saying the thing."""
                result = ask_claude(sp, f"Emoji: {emoji_input}\nContext: {emoji_context}", 900)
                save_history("🔢 Emoji Translator", emoji_input, result)
                st.session_state.emoji_quick = ""
            show_result(result)

    # ── 😶 SILENCE DECODER ───────────────────────────────────────────────────
    elif page == "😶 Silence Decoder":
        st.markdown("<h1>😶 SILENCE DECODER</h1>", unsafe_allow_html=True)
        mode_badge("⚡ COMEDY MODE")
        st.caption("She's not talking. Which is somehow LOUDER than talking.")

        c1, c2 = st.columns(2)
        with c1:
            duration  = st.selectbox("Duration of silence:", [
                "15–30 minutes", "1–2 hours", "Half a day", "Since yesterday",
                "2–3 days", "I can't remember her last words"])
            last_said = st.text_input("Last thing she said:", placeholder='"Fine." / "Okay." / [nothing]')
        with c2:
            trigger   = st.text_area("What happened before the silence?", height=100,
                            placeholder="e.g. I said I was watching cricket instead of helping with groceries")

        silence_clues = st.multiselect("Describe the silence:", [
            "Same room, zero words",        "Moved to another room",
            "One-word texts only",          "Read receipts, no reply",
            "Talking to everyone else normally",
            "She cried at some point",      "Polite but cold",
            "Busy on phone but not with me",
        ])

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            decode_sil = st.button("🔊 DECODE THE SILENCE", use_container_width=True)

        if decode_sil:
            with st.spinner("Amplifying the silence..."):
                sp = f"""You are a silence analyst specialising in {rel_type.lower()} communication — where nothing is said but everything is communicated.

### 🔕 SILENCE TYPE
Name it: Processing / Hurt / Punishing / Testing / Exhausted / Other. One-line description.

### 💭 WHAT'S HAPPENING IN HER HEAD
Be specific. Funny but accurate.

### ⏱️ THE DURATION FACTOR
What {duration} of silence specifically signals.

### 🔍 THE REAL ISSUE
What this silence is actually about (often not the surface trigger).

### ☢️ THREAT LEVEL
🟢 Needs space / 🟡 Needs acknowledgement / 🔴 Needs conversation / ☢️ Emergency

### 🛠️ OPERATION: BREAK THE SILENCE
Step-by-step. What to do, say, and NOT say.

### 💀 WORST THINGS TO SAY RIGHT NOW
3 phrases that will make this worse. (These are probably the ones you want to say.)"""
                prompt = f"Duration: {duration}\nLast words: {last_said}\nTrigger: {trigger}\nClues: {', '.join(silence_clues) or 'Not specified'}"
                result = ask_claude(sp, prompt, 1200)
                save_history("😶 Silence Decoder", trigger or duration, result)
            show_result(result)


# ════════════════════════════════════════════════════════════════
#  S E R I O U S   M O D E
# ════════════════════════════════════════════════════════════════
else:

    # ── 🙏 APOLOGY WORKSHOP ──────────────────────────────────────────────────
    if page == "🙏 Apology Workshop":
        st.markdown("<h1>🙏 Apology Workshop</h1>", unsafe_allow_html=True)
        mode_badge("SERIOUS MODE")
        st.caption("A good apology is a skill. Most people do it wrong. This helps you do it right.")
        st.info("A real apology has three parts: acknowledgement of what you did, understanding of its impact on her, and a genuine commitment to change. This tool builds all three.")

        what_happened = st.text_area("What happened? (be honest with yourself first)", height=110,
            placeholder="Describe what you did — not your justification for it, just what happened.")
        her_reaction = st.text_input(f"How has {rel_label} responded?",
            placeholder="e.g. She went quiet / She said she was hurt / She told me directly")

        c1, c2 = st.columns(2)
        with c1:
            severity = st.selectbox("How significant was this?", [
                "Minor — a slip or oversight",
                "Moderate — caused real hurt",
                "Significant — broke trust or a commitment",
                "Serious — this has happened before",
            ])
        with c2:
            apology_style = st.selectbox("Delivery:", [
                "Spoken, face to face",  "Written note or card",
                "Text message",          "Long heartfelt letter",
            ])

        apology_given = st.checkbox("I've already tried to apologise (didn't land well)")
        apology_how   = ""
        if apology_given:
            apology_how = st.text_input("What did you say?",
                placeholder="e.g. Said 'I'm sorry you felt that way'")

        if st.button("🙏 Build My Apology", use_container_width=True):
            if not validate(what_happened, "What happened"): st.stop()
            with st.spinner("Working through this thoughtfully..."):
                sp = f"""You are a relationship counsellor helping someone craft a genuine, effective apology to their {rel_type.lower()} ({rel_label}), together {years} years.

The goal is a REAL apology — not conflict avoidance. Focus on genuine accountability.

### What She Needs To Hear
Not what he wants to say — what she needs to receive emotionally to feel genuinely heard and respected.

### The Apology
Write the full apology for {apology_style} format. Make it:
- Specific to what actually happened (not generic)
- Acknowledging the impact, not just the action
- Free of "but" and "if you felt" qualifiers
- Natural sounding, not scripted

### Why This Works
What elements of a real apology this contains and why they matter.

### What To Do Alongside It
2–3 concrete actions that show the apology is genuine, not just words.

### Phrases That Undermine Apologies
4–5 things NOT to say — explain briefly why each one backfires.

### Realistic Expectations
Honest note on recovery given: {severity}. The difference between forgiven and forgotten.

Warm, direct, genuinely helpful."""
                apology_note = f"\nPrevious attempt: {apology_how}" if apology_given and apology_how else ""
                result = ask_claude(sp, f"What happened: {what_happened}\nHer response: {her_reaction}\nSeverity: {severity}{apology_note}", 1500)
                save_history("🙏 Apology Workshop", what_happened[:80], result)
            show_result(result)

    # ── ⚖️ ARGUMENT REFEREE ───────────────────────────────────────────────────
    elif page == "⚖️ Argument Referee":
        st.markdown("<h1>⚖️ Argument Referee</h1>", unsafe_allow_html=True)
        mode_badge("SERIOUS MODE")
        st.caption("A neutral outside perspective. The verdict might not go your way — that's the point.")

        topic = st.text_input("What is the argument about?",
            placeholder="e.g. Division of household tasks / How we spend weekends / Something specific that was said")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Your position**")
            your_side = st.text_area("What you said / believe:", height=120, key="ys",
                placeholder="Your side — as honestly as you can manage.")
        with c2:
            st.markdown(f"**{rel_label.capitalize()}'s position**")
            her_side = st.text_area("What she said / believes:", height=120, key="hs",
                placeholder="Her side — try to represent it fairly.")

        how_long_arg = st.selectbox("How long has this been an issue?",
            ["First time", "Come up before", "Recurring pattern", "Ongoing for a long time"])

        if st.button("⚖️ Get A Fair Reading", use_container_width=True):
            if not validate(topic, "The topic"): st.stop()
            with st.spinner("Reading both sides carefully..."):
                sp = f"""You are a fair, thoughtful relationship mediator. Your job is genuine neutrality — not to make either person feel better, but to help them understand what's actually happening.

### What This Argument Is Really About
The underlying dynamic or unmet need beneath the surface topic.

### What's Valid — His Side
Specific points where his position has genuine merit.

### What's Valid — Her Side
Specific points where her position has genuine merit.

### The Honest Verdict
Who has the stronger argument and why — or if it's genuinely split. Be direct. If he's wrong, say so.

### What's Fuelling The Conflict
Behaviours or patterns on BOTH sides making this harder than it needs to be.

### A Path Forward
Specific, actionable steps to resolve THIS argument — not generic "communicate more".

### The Bigger Picture
If recurring: what does this point to that's worth addressing properly?

Honest, fair, specific. Not harsh but don't soften to the point of uselessness."""
                result = ask_claude(sp, f"Topic: {topic}\nHis position: {your_side}\nHer position: {her_side}\nPattern: {how_long_arg}", 1400)
                save_history("⚖️ Argument Referee", topic, result)
            show_result(result)

    # ── 🎁 GIFT ADVISOR ───────────────────────────────────────────────────────
    elif page == "🎁 Gift Advisor":
        st.markdown("<h1>🎁 Gift Advisor</h1>", unsafe_allow_html=True)
        mode_badge("SERIOUS MODE")
        st.caption("The best gifts show you were paying attention. This helps you think it through properly.")

        c1, c2 = st.columns(2)
        with c1:
            occasion = st.selectbox("Occasion:", [
                "Apology / Making it right",        "Anniversary",
                "Birthday",                         "Just because — no occasion",
                "She's had a hard time lately",     "Celebrating something she achieved",
                "Reconnecting after distance",
            ])
            budget = st.selectbox("Budget:", ["Under $50", "$50–150", "$150–300", "$300–500", "$500+"])
        with c2:
            her_interests = st.text_input("Her interests / things she loves:",
                placeholder="e.g. cooking, reading, plants, long baths, a specific author")
            recent_context = st.text_area("Anything relevant lately?", height=88,
                placeholder="e.g. She mentioned wanting to learn something / She's been stressed / She gave something up recently")

        if st.button("🎁 Get Thoughtful Ideas", use_container_width=True):
            with st.spinner("Thinking this through..."):
                sp = f"""You are a thoughtful gift advisor for a {rel_type.lower()} ({rel_label}), together {years} years.

The best gifts are specific, personal, and show you pay attention. Avoid generic.

### What This Occasion Calls For
What kind of gift energy fits this specific situation — and why.

### Three Considered Recommendations
For each:
- What it is and why it fits HER specifically (use her interests and context)
- How to present it so it actually lands
- Realistic cost

### The Thoughtful Detail
One small, low-cost addition that shows real attention — a note, a specific memory referenced, a detail from something she mentioned.

### What To Avoid
2–3 gift types that would miss the mark for this occasion and person.

### A Note on Presentation
How to give it — timing, wrapping, what to say when you give it.

Specific and warm. The goal is a gift that says "I know you", not "I got you something"."""
                result = ask_claude(sp, f"Occasion: {occasion}\nBudget: {budget}\nInterests: {her_interests}\nContext: {recent_context}", 1300)
                save_history("🎁 Gift Advisor", f"{occasion} / {budget}", result)
            show_result(result)

    # ── 📅 DATE PLANNER ───────────────────────────────────────────────────────
    elif page == "📅 Date Planner":
        st.markdown("<h1>📅 Date Planner</h1>", unsafe_allow_html=True)
        mode_badge("SERIOUS MODE")
        st.caption("Worth planning well. The effort shows.")

        c1, c2 = st.columns(2)
        with c1:
            rel_state = st.selectbox("How are things between you right now?", [
                "Good — this is a treat",
                "Neutral — need some quality time",
                "A bit distant — need to reconnect",
                "After a rough patch — a fresh start",
            ])
            location = st.text_input("Your city:", placeholder="e.g. Sydney")
        with c2:
            budget_date = st.selectbox("Budget:", ["Under $50", "$50–150", "$150–300", "$300+"])
            constraints = st.multiselect("Constraints:", [
                "Have kids / need babysitter consideration",
                "Weeknight only", "Daytime only",
                "She hates loud / crowded places", "Outdoors preferred",
                "She's stressed — needs something low-key",
            ])

        her_prefs = st.text_input("What does she enjoy?",
            placeholder="e.g. good food, walks, trying new things, quiet evenings, live music")

        if st.button("📅 Plan A Good Date", use_container_width=True):
            with st.spinner("Planning something worth the effort..."):
                sp = f"""You are helping plan a genuinely good date for a couple — {rel_type.lower()}, {years} years together, in {location or 'Sydney, Australia'}.

Current state: {rel_state}. Tailor the date TYPE to match.

### The Right Kind of Date for Right Now
Given where things are, what KIND of experience will actually land — and why.

### A Considered Plan
A real itinerary. Specific kinds of venues (not just "a nice restaurant" — what vibe, what neighbourhood). Include:
- How to set it up and invite her
- Rough timing
- 2–3 conversation moments or shared activities that create genuine connection

### The Detail That Makes It
One specific thing — a gesture, a callback to something she loves, a moment to create — that elevates it from nice to memorable.

### What To Avoid
Based on her preferences and current relationship state.

### Budget Guide
How to spend the budget well.

Practical and warm. The goal is genuine connection, not just a nice outing."""
                result = ask_claude(sp, f"State: {rel_state}\nBudget: {budget_date}\nConstraints: {', '.join(constraints) or 'None'}\nPreferences: {her_prefs}", 1300)
                save_history("📅 Date Planner", rel_state, result)
            show_result(result)

    # ── 🌡️ RELATIONSHIP CHECK-IN ─────────────────────────────────────────────
    elif page == "🌡️ Relationship Check-in":
        st.markdown("<h1>🌡️ Relationship Check-in</h1>", unsafe_allow_html=True)
        mode_badge("SERIOUS MODE")
        st.caption("A periodic check-in is a healthy habit — worth doing when things are good, not just when they're not.")

        q1 = st.slider("Arguments / friction in the last month (0 = none, 10 = a lot):", 0, 10, 2)
        q2 = st.slider("How well are you communicating right now? (1 = poorly, 10 = very well):", 1, 10, 6)
        q3 = st.slider("How connected do you feel? (1–10):", 1, 10, 6)
        q4 = st.slider("How satisfied do you think SHE is right now? (1–10):", 1, 10, 6)
        q5 = st.slider("How satisfied are YOU right now? (1–10):", 1, 10, 7)

        c1, c2 = st.columns(2)
        with c1:
            quality_time = st.selectbox("Quality time together lately:", ["None", "Very little", "Some", "A good amount"])
            affection    = st.selectbox("Affection levels:", ["Very low", "Low", "Normal", "High"])
        with c2:
            going_well = st.text_input("What's genuinely going well:",
                placeholder="e.g. We laugh a lot / Good teamwork with the kids / She feels supported")
            needs_work = st.text_input("What you know needs more attention:",
                placeholder="e.g. Not much time alone / I've been distracted with work")

        if st.button("🌡️ Get An Honest Read", use_container_width=True):
            with st.spinner("Reading the full picture..."):
                score = round((q2 + q3 + q4 + q5) / 4 - (q1 * 0.25), 1)
                sp = """You are a thoughtful relationship counsellor giving an honest, constructive check-in. Not alarmist, not falsely reassuring.

### Where Things Are Right Now
An honest one-paragraph assessment — name what the numbers and context suggest, both positive and concerning.

### What's Working
Specific strengths based on what they've shared. Not generic.

### What Needs Attention
1–3 specific areas, with context for why each matters. Not a lecture.

### One Thing This Week
The single most high-leverage thing they could do in the next 7 days. Specific and achievable.

### A Longer View
If these patterns continue — where does this relationship go in 6 months? Be honest.

### A Note
One warm, direct observation about this couple based on everything shared.

Tone: warm and honest, like a trusted friend with real perspective. Not a therapy script."""
                prompt = f"Friction: {q1}/10, Communication: {q2}/10, Connection: {q3}/10\nHer satisfaction: {q4}/10, My satisfaction: {q5}/10\nQuality time: {quality_time}, Affection: {affection}\nGoing well: {going_well or 'Not mentioned'}\nNeeds work: {needs_work or 'Not mentioned'}"
                result = ask_claude(sp, prompt, 1400)
                save_history("🌡️ Relationship Check-in", f"Score ~{score}/10", result)

            st.metric("Indicative score", f"{score} / 10",
                help="Based on your inputs. Not a scientific measurement — use as a starting point.")
            show_result(result)


# ════════════════════════════════════════════════════════════════
#  S H A R E D :   H I S T O R Y
# ════════════════════════════════════════════════════════════════
if page == "🕑 History":
    if mode == "comedy":
        st.markdown("<h1>🕑 SESSION LOG</h1>", unsafe_allow_html=True)
        mode_badge("⚡ COMEDY MODE")
    else:
        st.markdown("<h1>🕑 Session History</h1>", unsafe_allow_html=True)
        mode_badge("SERIOUS MODE")

    if not st.session_state.history:
        st.info("Nothing yet. Use any feature and your results will appear here.")
    else:
        c1, c2 = st.columns([1, 4])
        with c1:
            if st.button("🗑️ Clear all", use_container_width=True):
                for k in ["history", "phrase_result", "phrase_current"]:
                    st.session_state[k] = [] if k == "history" else None
                st.rerun()
        st.caption(f"{len(st.session_state.history)} reading(s) this session")

        for item in st.session_state.history:
            tag = "😂" if item.get("mode") == "comedy" else "🧠"
            with st.expander(f"{tag}  {item['feature']}  ·  {item['time']}  ·  \"{item['input']}\""):
                st.markdown(item["result"])
