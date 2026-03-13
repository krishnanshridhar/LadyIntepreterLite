import streamlit as st
from datetime import datetime
import os
import re

st.set_page_config(
    page_title="She Said What?",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in {
    "mode": "comedy", "page": None, "history": [],
    "phrase_result": None, "phrase_current": None, "emoji_quick": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

mode = st.session_state.mode

# ── CSS — targets Streamlit shell + widgets only ──────────────────────────────
COMEDY_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
.stApp { background: #FFFFFF !important; }
.block-container { padding: 0 2rem 3rem !important; max-width: 800px !important; }

/* Sidebar */
section[data-testid="stSidebar"] > div:first-child { background: #111111 !important; }
section[data-testid="stSidebar"] * { color: #FFFFFF !important; font-family: 'DM Sans', sans-serif !important; }
section[data-testid="stSidebar"] hr { border-color: #333333 !important; opacity: 1 !important; }
section[data-testid="stSidebar"] input { background: #222222 !important; border-color: #444444 !important; color: #FFFFFF !important; }
section[data-testid="stSidebar"] input::placeholder { color: #888888 !important; }
section[data-testid="stSidebar"] [data-baseweb="select"] > div { background: #222222 !important; border-color: #444444 !important; }
section[data-testid="stSidebar"] [data-baseweb="select"] span { color: #FFFFFF !important; }
section[data-testid="stSidebar"] [data-testid="stSlider"] * { color: #DDDDDD !important; }
section[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div { background: #444444 !important; }
section[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div > div { background: #FFCC00 !important; }

/* Widget labels */
[data-testid="stWidgetLabel"] p { color: #111111 !important; font-weight: 600 !important; font-size: 0.88rem !important; letter-spacing: 0.1px !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: #FAFAFA !important; border: 1.5px solid #DDDDDD !important;
    border-radius: 8px !important; color: #111111 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.95rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #111111 !important; box-shadow: none !important; }
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #999999 !important; opacity: 1 !important; }

/* Select */
[data-baseweb="select"] > div { background: #FAFAFA !important; border: 1.5px solid #DDDDDD !important; border-radius: 8px !important; }
[data-baseweb="select"] span { color: #111111 !important; }
[data-baseweb="option"] { background: #FFFFFF !important; color: #111111 !important; }
[data-baseweb="option"]:hover { background: #FFF8EC !important; }
[data-baseweb="tag"] { background: #111111 !important; border-radius: 4px !important; }
[data-baseweb="tag"] span { color: #FFFFFF !important; }

/* Sliders */
[data-testid="stSlider"] [data-testid="stWidgetLabel"] p { color: #111111 !important; }
[data-testid="stSlider"] > div > div > div > div { background: #EEEEEE !important; }
[data-testid="stSlider"] > div > div > div > div > div { background: #111111 !important; }
[data-testid="stThumbValue"], [data-testid="stTickBarMin"], [data-testid="stTickBarMax"] { color: #666666 !important; font-size: 0.78rem !important; }

/* Checkbox / radio */
.stCheckbox > label > div > p, .stRadio > div > label > div > p { color: #111111 !important; font-size: 0.9rem !important; }

/* Button */
.stButton > button {
    background: #111111 !important; color: #FFFFFF !important; border: none !important;
    border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    padding: 0.6rem 1.5rem !important; width: 100% !important;
    transition: background 0.15s, transform 0.1s !important;
}
.stButton > button:hover { background: #2A2A2A !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* Expanders */
[data-testid="stExpander"] { border: 1.5px solid #EEEEEE !important; border-radius: 10px !important; background: #FAFAFA !important; }
[data-testid="stExpander"] summary p { color: #111111 !important; font-weight: 600 !important; font-size: 0.88rem !important; }

/* Alert */
[data-testid="stAlert"] { background: #FFF8EC !important; border: 1.5px solid #DDDDDD !important; border-radius: 8px !important; }
[data-testid="stAlert"] p { color: #111111 !important; font-weight: 500 !important; }

/* Metric */
[data-testid="stMetric"] { background: #FFF8EC !important; border: 1.5px solid #EEEEEE !important; border-radius: 10px !important; padding: 1rem !important; }
[data-testid="stMetricLabel"] p { color: #666666 !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
[data-testid="stMetricValue"] { color: #111111 !important; font-family: 'Syne', sans-serif !important; }
[data-testid="stSpinner"] p { color: #666666 !important; }

@media (max-width: 768px) {
    .block-container { padding: 0 1rem 2rem !important; }
    div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
}
"""

SERIOUS_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }
.stApp { background: #F6F3EE !important; }
.block-container { padding: 0 2rem 3rem !important; max-width: 800px !important; }

/* Sidebar */
section[data-testid="stSidebar"] > div:first-child { background: #EAE6DF !important; }
section[data-testid="stSidebar"] * { color: #1A1208 !important; font-family: 'DM Sans', sans-serif !important; }
section[data-testid="stSidebar"] hr { border-color: #CEC8BF !important; opacity: 1 !important; }
section[data-testid="stSidebar"] input { background: #F6F3EE !important; border-color: #CEC8BF !important; color: #1A1208 !important; }
section[data-testid="stSidebar"] input::placeholder { color: #8A8178 !important; }
section[data-testid="stSidebar"] [data-baseweb="select"] > div { background: #F6F3EE !important; border-color: #CEC8BF !important; }
section[data-testid="stSidebar"] [data-baseweb="select"] span { color: #1A1208 !important; }
section[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div { background: #CEC8BF !important; }
section[data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div > div { background: #2D6A4F !important; }

/* Widget labels */
[data-testid="stWidgetLabel"] p { color: #1A1208 !important; font-weight: 600 !important; font-size: 0.88rem !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea {
    background: #FFFFFF !important; border: 1.5px solid #CEC8BF !important;
    border-radius: 8px !important; color: #1A1208 !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.95rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #2D6A4F !important; box-shadow: 0 0 0 3px rgba(45,106,79,0.1) !important; }
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #9A9188 !important; opacity: 1 !important; }

/* Select */
[data-baseweb="select"] > div { background: #FFFFFF !important; border: 1.5px solid #CEC8BF !important; border-radius: 8px !important; }
[data-baseweb="select"] span { color: #1A1208 !important; }
[data-baseweb="option"] { background: #FFFFFF !important; color: #1A1208 !important; }
[data-baseweb="option"]:hover { background: #F0EDE7 !important; }
[data-baseweb="tag"] { background: rgba(45,106,79,0.12) !important; border-radius: 4px !important; }
[data-baseweb="tag"] span { color: #1A4A34 !important; font-weight: 600 !important; }

/* Sliders */
[data-testid="stSlider"] [data-testid="stWidgetLabel"] p { color: #1A1208 !important; }
[data-testid="stSlider"] > div > div > div > div { background: #D8D2C8 !important; }
[data-testid="stSlider"] > div > div > div > div > div { background: #2D6A4F !important; }
[data-testid="stThumbValue"], [data-testid="stTickBarMin"], [data-testid="stTickBarMax"] { color: #5C5650 !important; font-size: 0.78rem !important; }

/* Checkbox / radio */
.stCheckbox > label > div > p, .stRadio > div > label > div > p { color: #1A1208 !important; font-size: 0.9rem !important; }

/* Button */
.stButton > button {
    background: #2D6A4F !important; color: #FFFFFF !important; border: none !important;
    border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    padding: 0.6rem 1.5rem !important; width: 100% !important;
    transition: background 0.15s, transform 0.1s !important;
}
.stButton > button:hover { background: #235C41 !important; transform: translateY(-1px) !important; }

/* Expanders */
[data-testid="stExpander"] { background: #FFFFFF !important; border: 1.5px solid #E0DAD2 !important; border-radius: 10px !important; }
[data-testid="stExpander"] summary p { color: #1A1208 !important; font-weight: 600 !important; font-size: 0.88rem !important; }

/* Alert */
[data-testid="stAlert"] { background: #F0F7F4 !important; border: 1.5px solid #2D6A4F !important; border-left-width: 4px !important; border-radius: 8px !important; }
[data-testid="stAlert"] p { color: #1A3D2C !important; font-weight: 500 !important; }

/* Metric */
[data-testid="stMetric"] { background: #FFFFFF !important; border: 1.5px solid #E0DAD2 !important; border-radius: 10px !important; padding: 1rem !important; }
[data-testid="stMetricLabel"] p { color: #5C5650 !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
[data-testid="stMetricValue"] { color: #2D6A4F !important; font-family: 'Syne', sans-serif !important; }
[data-testid="stSpinner"] p { color: #5C5650 !important; }

@media (max-width: 768px) {
    .block-container { padding: 0 1rem 2rem !important; }
    div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; }
}
"""

st.markdown("<style>" + (COMEDY_CSS if mode == "comedy" else SERIOUS_CSS) + "</style>",
            unsafe_allow_html=True)

# ── API KEY ───────────────────────────────────────────────────────────────────
api_key = os.environ.get("ANTHROPIC_API_KEY", "")
if not api_key:
    st.error("**ANTHROPIC_API_KEY not set.**\n\nRun: `ANTHROPIC_API_KEY=sk-... streamlit run app.py`\n\nStreamlit Cloud: Manage app → Secrets")
    st.stop()

import anthropic
client = anthropic.Anthropic(api_key=api_key)

# ── HELPERS ───────────────────────────────────────────────────────────────────
def ask_claude(system_prompt, user_msg, max_tokens=1200):
    try:
        resp = client.messages.create(
            model="claude-sonnet-4-5", max_tokens=max_tokens,
            system=system_prompt, messages=[{"role": "user", "content": user_msg}]
        )
        return resp.content[0].text
    except anthropic.AuthenticationError:
        return "❌ **Authentication error** — check your API key."
    except anthropic.RateLimitError:
        return "❌ **Rate limit** — wait a moment and try again."
    except anthropic.APIStatusError as e:
        return "❌ **API error** — " + str(e.message)
    except Exception as e:
        return "❌ **Error** — " + str(e)

def save_history(feature, input_text, result):
    snippet = input_text[:100] + ("..." if len(input_text) > 100 else "")
    st.session_state.history.insert(0, {
        "feature": feature, "input": snippet, "result": result,
        "time": datetime.now().strftime("%d %b %H:%M"), "mode": mode,
    })
    st.session_state.history = st.session_state.history[:20]

def validate(text, label="This field"):
    if not text.strip():
        st.warning("⚠️  " + label + " can't be empty.")
        return False
    return True

def md_to_html(text):
    """Convert markdown to HTML for rendering inside our styled divs."""
    # Code blocks
    text = re.sub(r'```[a-z]*\n?(.*?)```', lambda m: '<code>' + m.group(1).strip() + '</code>', text, flags=re.DOTALL)
    # H3 and H2
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$',  r'<h3>\1</h3>', text, flags=re.MULTILINE)
    # Bold / italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.+?)__',     r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Numbered lists
    def make_ol(m):
        items = re.findall(r'^\d+\.\s+(.+)$', m.group(0), re.MULTILINE)
        return '<ol>' + ''.join('<li>' + i + '</li>' for i in items) + '</ol>'
    text = re.sub(r'(^\d+\..+$\n?)+', make_ol, text, flags=re.MULTILINE)
    # Bullet lists
    def make_ul(m):
        items = re.findall(r'^[-*]\s+(.+)$', m.group(0), re.MULTILINE)
        return '<ul>' + ''.join('<li>' + i + '</li>' for i in items) + '</ul>'
    text = re.sub(r'(^[-*]\s+.+$\n?)+', make_ul, text, flags=re.MULTILINE)
    # Wrap bare lines in <p>
    lines, out = text.split('\n'), []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('<'):
            out.append(s)
        else:
            out.append('<p>' + s + '</p>')
    return '\n'.join(out)

# ── DESIGN COMPONENTS  ───────────────────────────────────────────────────────
def C():
    if mode == "comedy":
        return {"accent": "#111111", "accent_bg": "#FFCC00", "accent_text": "#111111",
                "text": "#111111", "muted": "#666666", "bg": "#FFFFFF",
                "surface": "#FAFAFA", "border": "#EEEEEE", "tag_tc": "#111111"}
    return {"accent": "#2D6A4F", "accent_bg": "#2D6A4F", "accent_text": "#FFFFFF",
            "text": "#1A1208", "muted": "#5C5650", "bg": "#F6F3EE",
            "surface": "#FFFFFF", "border": "#E0DAD2", "tag_tc": "#FFFFFF"}

def page_header(title, subtitle=""):
    c = C()
    tag_label = "COMEDY" if mode == "comedy" else "SERIOUS"
    tag_html = (
        "<span style='background:" + c["accent_bg"] + ";color:" + c["accent_text"] + ";"
        "font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;"
        "padding:3px 10px;border-radius:3px;font-family:DM Sans,sans-serif;'>"
        + tag_label + "</span>"
    )
    sub_html = ""
    if subtitle:
        sub_html = (
            "<p style='margin:6px 0 0;font-size:0.9rem;color:" + c["muted"] + ";"
            "font-family:DM Sans,sans-serif;line-height:1.5;'>" + subtitle + "</p>"
        )
    h1_html = (
        "<h1 style='font-family:Syne,sans-serif;font-size:2rem;font-weight:800;"
        "color:" + c["text"] + ";margin:10px 0 0;letter-spacing:-0.5px;line-height:1.15;'>"
        + title + "</h1>"
    )
    st.markdown(
        "<div style='padding:2rem 0 1.4rem;border-bottom:2px solid " + c["border"] + ";margin-bottom:1.6rem;'>"
        + tag_html + h1_html + sub_html + "</div>",
        unsafe_allow_html=True
    )

def callout(text, variant="info"):
    c = C()
    if mode == "comedy":
        bg, border, tc = "#FFF8EC", "#FFCC00", "#111111"
    else:
        palettes = {
            "info":    ("#F0F7F4", "#2D6A4F", "#1A3D2C"),
            "warning": ("#FFF8F0", "#C8622A", "#5C2A0A"),
            "tip":     ("#F6F3EE", "#CEC8BF", "#3A3028"),
        }
        bg, border, tc = palettes.get(variant, palettes["info"])
    st.markdown(
        "<div style='background:" + bg + ";border:1.5px solid " + border + ";"
        "border-radius:8px;padding:0.9rem 1.1rem;margin:0 0 1.2rem;'>"
        "<p style='margin:0;color:" + tc + ";font-size:0.9rem;font-weight:500;"
        "font-family:DM Sans,sans-serif;line-height:1.6;'>" + text + "</p></div>",
        unsafe_allow_html=True
    )

def section_label(text):
    c = C()
    st.markdown(
        "<p style='font-family:DM Sans,sans-serif;font-size:0.75rem;font-weight:700;"
        "letter-spacing:1.5px;text-transform:uppercase;color:" + c["muted"] + ";"
        "margin:1.4rem 0 0.3rem;'>" + text + "</p>",
        unsafe_allow_html=True
    )

def show_result(result):
    c = C()
    if mode == "comedy":
        bl = "4px solid #FFCC00"
        h3c = "#111111"
    else:
        bl = "4px solid " + c["accent"]
        h3c = c["accent"]
    inner = md_to_html(result)
    styles = (
        "<style>"
        ".ssw-result{background:" + c["surface"] + ";border:1.5px solid " + c["border"] + ";"
        "border-left:" + bl + ";border-radius:10px;padding:1.8rem 2rem;margin:1.5rem 0;"
        "font-family:'DM Sans',sans-serif;}"
        ".ssw-result h3{font-family:'Syne',sans-serif!important;color:" + h3c + "!important;"
        "font-size:0.92rem!important;font-weight:800!important;text-transform:uppercase!important;"
        "letter-spacing:1px!important;margin:1.4rem 0 0.5rem!important;"
        "padding-bottom:4px!important;border-bottom:1px solid " + c["border"] + "!important;}"
        ".ssw-result h3:first-child{margin-top:0!important;}"
        ".ssw-result p{color:" + c["text"] + "!important;font-size:0.95rem!important;"
        "margin:0 0 0.7rem!important;line-height:1.75!important;}"
        ".ssw-result li{color:" + c["text"] + "!important;font-size:0.95rem!important;"
        "margin-bottom:0.35rem!important;line-height:1.7!important;}"
        ".ssw-result ul,.ssw-result ol{padding-left:1.4rem!important;margin:0 0 0.7rem!important;}"
        ".ssw-result strong{color:" + c["text"] + "!important;font-weight:700!important;}"
        ".ssw-result em{color:" + c["muted"] + "!important;}"
        ".ssw-result code{background:" + c["border"] + "!important;padding:1px 6px!important;"
        "border-radius:3px!important;font-size:0.88rem!important;}"
        "</style>"
    )
    st.markdown(styles + "<div class='ssw-result'>" + inner + "</div>", unsafe_allow_html=True)

def fdivider():
    c = C()
    st.markdown(
        "<div style='height:1px;background:" + c["border"] + ";margin:1.5rem 0;'></div>",
        unsafe_allow_html=True
    )

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if mode == "comedy":
        st.markdown(
            "<h2 style='font-family:Syne,sans-serif;font-size:1.25rem;font-weight:800;"
            "margin-bottom:2px;color:#FFFFFF;'>She Said What?</h2>"
            "<p style='font-size:0.75rem;opacity:0.5;margin-top:0;color:#FFFFFF;'>Relationship survival toolkit</p>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<h2 style='font-family:Syne,sans-serif;font-size:1.25rem;font-weight:800;"
            "margin-bottom:2px;color:#1A1208;'>She Said What?</h2>"
            "<p style='font-size:0.75rem;color:#5C5650;margin-top:0;'>Relationship tools</p>",
            unsafe_allow_html=True
        )

    st.divider()

    # Mode toggle
    if mode == "comedy":
        st.markdown("<p style='font-size:0.7rem;font-weight:700;letter-spacing:1.5px;"
                    "text-transform:uppercase;opacity:0.5;margin-bottom:4px;'>Mode</p>",
                    unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:0.7rem;font-weight:700;letter-spacing:1.5px;"
                    "text-transform:uppercase;color:#5C5650;margin-bottom:4px;'>Mode</p>",
                    unsafe_allow_html=True)

    ca, cb = st.columns(2)
    with ca:
        if st.button("😂 Comedy", use_container_width=True, key="btn_comedy"):
            st.session_state.mode = "comedy"
            st.session_state.page = None
            st.session_state.phrase_result = None
            st.rerun()
    with cb:
        if st.button("🧠 Serious", use_container_width=True, key="btn_serious"):
            st.session_state.mode = "serious"
            st.session_state.page = None
            st.session_state.phrase_result = None
            st.rerun()

    if mode == "comedy":
        st.markdown("<p style='font-size:0.72rem;opacity:0.4;margin-top:3px;'>For laughs. May cause recognition.</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:0.72rem;color:#8A8178;margin-top:3px;'>For moments that actually matter.</p>", unsafe_allow_html=True)

    st.divider()

    # Personalise
    if mode == "comedy":
        st.markdown("<p style='font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;opacity:0.5;margin-bottom:6px;'>Personalise</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#5C5650;margin-bottom:6px;'>Personalise</p>", unsafe_allow_html=True)

    her_name  = st.text_input("Her name / nickname", value="her",  key="sb_her")
    your_name = st.text_input("Your name",           value="me",   key="sb_you")
    rel_type  = st.selectbox("Relationship", ["Wife","Girlfriend","Fiancée","Partner"], key="sb_rel")
    years     = st.slider("Years together", 0, 30, 2, key="sb_yrs")

    st.divider()

    # Navigation
    if mode == "comedy":
        st.markdown("<p style='font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;opacity:0.5;margin-bottom:4px;'>Features</p>", unsafe_allow_html=True)
        nav_items = [
            ("💬", "What She Really Said"),
            ("📖", "The Phrase Bible"),
            ("🚨", "Danger Meter"),
            ("🔢", "Emoji Translator"),
            ("😶", "Silence Decoder"),
            ("🕑", "History"),
        ]
    else:
        st.markdown("<p style='font-size:0.7rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#5C5650;margin-bottom:4px;'>Features</p>", unsafe_allow_html=True)
        nav_items = [
            ("🙏", "Apology Workshop"),
            ("⚖️",  "Argument Referee"),
            ("🎁", "Gift Advisor"),
            ("📅", "Date Planner"),
            ("🌡️", "Relationship Check-in"),
            ("🕑", "History"),
        ]

    for icon, label in nav_items:
        full_key = icon + " " + label
        is_active = (st.session_state.page == full_key)
        if is_active:
            if mode == "comedy":
                bg_nav = "#FFCC00"; tc_nav = "#111111"; fw_nav = "700"
            else:
                bg_nav = "#2D6A4F"; tc_nav = "#FFFFFF"; fw_nav = "700"
        else:
            bg_nav = "transparent"
            tc_nav = "rgba(255,255,255,0.65)" if mode == "comedy" else "rgba(26,18,8,0.6)"
            fw_nav = "400"

        st.markdown(
            "<div style='background:" + bg_nav + ";border-radius:6px;padding:1px 0;margin:1px 0;'>"
            "<span style='font-family:DM Sans,sans-serif;font-size:0.88rem;"
            "color:" + tc_nav + ";font-weight:" + fw_nav + ";padding:6px 10px;display:block;'>"
            + icon + "&nbsp;&nbsp;" + label + "</span></div>",
            unsafe_allow_html=True
        )
        if st.button(label, key="nav_" + label, use_container_width=True):
            st.session_state.page = full_key
            st.rerun()

    st.divider()
    if mode == "comedy":
        st.markdown("<p style='font-size:0.7rem;opacity:0.35;text-align:center;'>For entertainment only 😄</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='font-size:0.7rem;color:#8A8178;text-align:center;'>Best used for genuine moments</p>", unsafe_allow_html=True)


# ── ROUTE ─────────────────────────────────────────────────────────────────────
rel_label = her_name.strip() if her_name.strip() not in ("", "her") else rel_type.lower()
page      = st.session_state.page

# ── LANDING PAGE ──────────────────────────────────────────────────────────────
if page is None:
    c = C()
    if mode == "comedy":
        features_html = "".join(
            "<span style='background:#F5F5F5;border:1.5px solid #EEEEEE;padding:7px 14px;"
            "border-radius:6px;font-size:0.83rem;font-family:DM Sans,sans-serif;color:#333333;'>"
            + icon + " " + label + "</span>"
            for icon, label in [
                ("💬","What She Really Said"),("📖","Phrase Bible"),
                ("🚨","Danger Meter"),("🔢","Emoji Translator"),("😶","Silence Decoder")
            ]
        )
        st.markdown(
            "<div style='padding:3rem 0 2rem;'>"
            "<span style='background:#FFCC00;color:#111111;font-size:0.7rem;font-weight:700;"
            "letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border-radius:3px;"
            "font-family:DM Sans,sans-serif;'>COMEDY MODE</span>"
            "<h1 style='font-family:Syne,sans-serif;font-size:2.6rem;font-weight:800;"
            "color:#111111;margin:14px 0 8px;letter-spacing:-1px;line-height:1.1;'>"
            "She said one thing.<br>She meant another.</h1>"
            "<p style='font-size:1rem;color:#555555;max-width:480px;line-height:1.7;"
            "font-family:DM Sans,sans-serif;margin-bottom:2rem;'>"
            "Five tools for decoding the messages, silences, and emojis "
            "that keep you up at night.</p>"
            "<div style='display:flex;gap:10px;flex-wrap:wrap;'>" + features_html + "</div>"
            "<p style='font-size:0.82rem;color:#999999;margin-top:1.5rem;"
            "font-family:DM Sans,sans-serif;'>← Pick a feature from the sidebar</p>"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        features_html = "".join(
            "<span style='background:#FFFFFF;border:1.5px solid #E0DAD2;padding:7px 14px;"
            "border-radius:6px;font-size:0.83rem;font-family:DM Sans,sans-serif;color:#3A3028;'>"
            + icon + " " + label + "</span>"
            for icon, label in [
                ("🙏","Apology Workshop"),("⚖️","Argument Referee"),
                ("🎁","Gift Advisor"),("📅","Date Planner"),("🌡️","Check-in")
            ]
        )
        st.markdown(
            "<div style='padding:3rem 0 2rem;'>"
            "<span style='background:#2D6A4F;color:#FFFFFF;font-size:0.7rem;font-weight:700;"
            "letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border-radius:3px;"
            "font-family:DM Sans,sans-serif;'>SERIOUS MODE</span>"
            "<h1 style='font-family:Syne,sans-serif;font-size:2.6rem;font-weight:800;"
            "color:#1A1208;margin:14px 0 8px;letter-spacing:-1px;line-height:1.1;'>"
            "Tools for the moments<br>that actually matter.</h1>"
            "<p style='font-size:1rem;color:#5C5650;max-width:480px;line-height:1.7;"
            "font-family:DM Sans,sans-serif;margin-bottom:2rem;'>"
            "Five practical tools for apologies, arguments, gifts, dates, "
            "and relationship check-ins.</p>"
            "<div style='display:flex;gap:10px;flex-wrap:wrap;'>" + features_html + "</div>"
            "<p style='font-size:0.82rem;color:#8A8178;margin-top:1.5rem;"
            "font-family:DM Sans,sans-serif;'>← Pick a feature from the sidebar</p>"
            "</div>",
            unsafe_allow_html=True
        )
    st.stop()

# ══════════════════════════════════════════
# COMEDY FEATURES
# ══════════════════════════════════════════
if mode == "comedy":

    if page == "💬 What She Really Said":
        page_header("What She Really Said", "She said one thing. She meant another. Let's find out what.")
        input_type = st.radio("Input type:", ["Single message", "Full conversation"], horizontal=True)
        if input_type == "Single message":
            msg     = st.text_area("What did " + rel_label + " say?", height=100,
                        placeholder='"Fine." / "Do whatever you want." / "I\'m not mad."')
            context = st.text_input("Context (optional):", placeholder="e.g. After I said I was going to watch cricket")
        else:
            msg     = st.text_area("Paste the conversation:", height=200, placeholder="Paste WhatsApp / iMessage chat here...")
            context = st.text_input("Context (optional):", placeholder="e.g. About weekend plans")
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            go = st.button("Decode it →", use_container_width=True)
        if go:
            if not validate(msg, "The message"): st.stop()
            with st.spinner("Reading between the lines..."):
                sp = (
                    "You are an accurate relationship translator — funny because you're uncomfortably right.\n"
                    + your_name + " is decoding a message from their " + rel_type.lower()
                    + " (" + rel_label + "), together " + str(years) + " year(s).\n\n"
                    "Use these exact section headings:\n\n"
                    "### 💬 What She Said\nQuote the key phrase(s) back.\n\n"
                    "### 🤔 What She Meant\nThe real message. Specific. No sugar-coating.\n\n"
                    "### 🌡️ Threat Level\n"
                    "ONE of: 🟢 Stand Down / 🟡 Proceed With Caution / 🔴 MAYDAY / ☢️ Abandon Ship\n"
                    "One-line reason.\n\n"
                    "### 🎯 Your Mission\n3 numbered, specific actions. Funny but actually useful.\n\n"
                    "### 💀 Do Not\n2 things that will make this significantly worse.\n\n"
                    "### 🏆 The Magic Words\nOne sentence they can say right now.\n\n"
                    "### 🔮 Prophecy\nRight-thing vs wrong-thing outcomes. Brief, funny, accurate."
                )
                prompt = "Message: " + msg + ("\nContext: " + context if context.strip() else "")
                result = ask_claude(sp, prompt, 1400)
                save_history("💬 What She Really Said", msg, result)
            show_result(result)

    elif page == "📖 The Phrase Bible":
        page_header("The Phrase Bible", "Sacred texts. Study them. Know them. Fear them.")
        classics = [
            "I'm fine.",                         "Do whatever you want.",
            "Nothing's wrong.",                  "We need to talk.",
            "It's okay.",                        "If you want to.",
            "I don't care.",                     "You never listen.",
            "Must be nice.",                     "Sure, go ahead.",
            "I'm not angry, I'm disappointed.",  "Forget it.",
            "No, don't worry about it.",         "Whatever.",
            "I'm tired.",                        "It's not a big deal.",
            "You wouldn't understand.",          "I already told you.",
        ]
        section_label("Classic phrases — click to decode")
        cols = st.columns(3)
        for i, phrase in enumerate(classics):
            with cols[i % 3]:
                if st.button('"' + phrase + '"', key="ph_" + str(i), use_container_width=True):
                    with st.spinner("Consulting the sacred texts..."):
                        sp = (
                            "Decode this classic " + rel_type.lower() + " phrase with insight and humour.\n\n"
                            "### 📖 The Phrase\nQuote it back.\n\n"
                            "### 😇 Official Meaning\nWhat it claims to mean (the lie).\n\n"
                            "### 💣 Actual Meaning\nWhat it really means — specific and funny.\n\n"
                            "### ☢️ Danger Rating\n🟢 Mild / 🟡 Watch It / 🔴 Danger Zone / ☢️ Full Nuclear\n\n"
                            "### 🎓 The Psychology\nOne sentence: WHY she says this instead of what she means.\n\n"
                            "### 🛡️ Survival Guide\n3 numbered tips. Funny but practical.\n\n"
                            "### 😂 Fun Fact\nOne genuinely funny observation about this phrase."
                        )
                        result = ask_claude(sp, 'Phrase: "' + phrase + '"')
                        st.session_state.phrase_result  = result
                        st.session_state.phrase_current = phrase
                        save_history("📖 Phrase Bible", phrase, result)
        if st.session_state.phrase_result:
            fdivider()
            st.caption('Decoded: "' + str(st.session_state.phrase_current) + '"')
            show_result(st.session_state.phrase_result)
        fdivider()
        section_label("Custom lookup")
        custom = st.text_input("Type any phrase:", placeholder='e.g. "Why would I be upset about that?"')
        if st.button("Look it up →", use_container_width=True):
            if validate(custom, "Phrase"):
                with st.spinner("Consulting the archives..."):
                    sp = "Decode this " + rel_type.lower() + " phrase. Format: Official Meaning, Actual Meaning, Danger Rating, Psychology, Survival Guide (3 tips), Fun Fact."
                    result = ask_claude(sp, 'Phrase: "' + custom + '"')
                    st.session_state.phrase_result  = result
                    st.session_state.phrase_current = custom
                    save_history("📖 Phrase Bible", custom, result)
                show_result(st.session_state.phrase_result)

    elif page == "🚨 Danger Meter":
        page_header("Danger Meter", "Describe your situation. Find out your survival probability.")
        situation = st.text_area("Situation report:", height=120,
            placeholder="e.g. Forgot our anniversary. She said 'It's fine' and went to bed at 8pm. This morning she made tea only for herself.")
        c1, c2 = st.columns(2)
        with c1:
            how_long = st.selectbox("Duration:", ["Just happened","A few hours","Since yesterday","2–3 days","A week+","I've completely lost track"])
        with c2:
            prev = st.selectbox("Prior offences:", ["First time","Once before","This is a pattern","I'm basically always in trouble"])
        section_label("Active red flags")
        red_flags = st.multiselect("Select all that apply:", [
            "She's gone quiet 🤐","One-word text replies","Unusually NICE 😬","She called her mum",
            "Aggressive cleaning 🧹","Made tea only for herself","Liked your friend's photo, not yours",
            "Said 'I'm fine' more than once","No goodnight kiss","'We need to talk' received",
            "Rearranging furniture","Watching sad movies alone",
        ])
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            assess = st.button("Assess threat level →", use_container_width=True)
        if assess:
            if not validate(situation, "Situation"): st.stop()
            with st.spinner("Running threat assessment..."):
                sp = (
                    "You are a hilariously blunt relationship danger analyst.\n\n"
                    "### 🚨 Threat Level\n"
                    "State: 🟢 STAND DOWN / 🟡 ELEVATED / 🔴 HIGH ALERT / ☢️ DEFCON 1\n"
                    "Score X/10. One dramatic headline.\n\n"
                    "### 🔍 Field Assessment\nWhat's actually happening — specific and funny.\n\n"
                    "### 📊 Threat Multipliers\nWhat's making this worse.\n\n"
                    "### 🛠️ Recovery Protocol\nNumbered steps. Specific, practical, with humour.\n\n"
                    "### 💀 Critical Errors\n3 things that will escalate from bad to catastrophic.\n\n"
                    "### 📈 Survival Probability\nA percentage with brief honest reasoning."
                )
                prompt = "Situation: " + situation + "\nDuration: " + how_long + "\nPattern: " + prev + "\nRed flags: " + (", ".join(red_flags) or "None")
                result = ask_claude(sp, prompt, 1300)
                save_history("🚨 Danger Meter", situation[:80], result)
            show_result(result)

    elif page == "🔢 Emoji Translator":
        page_header("Emoji Translator", "A single 🙂 from your partner contains multitudes.")
        quick_set = [
            ("🙂","The smile"),("👍","Thumbs up"),("😶","The void"),("🙄","Eye roll"),
            ("😤","The puff"),("🫠","Melting"),("❤️‍🩹","Hurt heart"),("🤔","Thinking"),
        ]
        section_label("Quick decode")
        qcols = st.columns(4)
        for i, (em, label) in enumerate(quick_set):
            with qcols[i % 4]:
                if st.button(em + "  " + label, key="eq_" + str(i), use_container_width=True):
                    st.session_state.emoji_quick = em
        emoji_input   = st.text_input("Emoji(s) to decode:", value=st.session_state.emoji_quick,
                            placeholder="Paste emoji(s) here — e.g. 😶👍 or just 🙂")
        emoji_context = st.text_input("Context:", placeholder="e.g. After I said I'd be home late")
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            decode_em = st.button("Decode these emojis →", use_container_width=True)
        if decode_em:
            if not validate(emoji_input, "Emoji input"): st.stop()
            with st.spinner("Running emoji forensics..."):
                sp = (
                    "You are a relationship emoji expert. A " + rel_type.lower() + "'s emoji is NEVER just an emoji.\n\n"
                    "### 📱 The Emoji(s)\nState what was sent.\n\n"
                    "### 😇 Claimed Meaning\nThe naive interpretation.\n\n"
                    "### 💣 Actual Meaning\nReal meaning in context — specific and funny.\n\n"
                    "### 🌡️ Emotional Reading\nWarm / Neutral / Passive-aggressive / Happy / Testing / Plotting\n\n"
                    "### ☢️ Danger Level\n🟢 Safe / 🟡 Caution / 🔴 Alert\n\n"
                    "### 💬 How To Respond\nAn actual reply they can send right now.\n\n"
                    "### 😂 The Deeper Truth\nWhy " + rel_type.lower() + "s communicate via emoji instead of just saying the thing."
                )
                result = ask_claude(sp, "Emoji: " + emoji_input + "\nContext: " + emoji_context, 900)
                save_history("🔢 Emoji Translator", emoji_input, result)
                st.session_state.emoji_quick = ""
            show_result(result)

    elif page == "😶 Silence Decoder":
        page_header("Silence Decoder", "She's not talking. Which is somehow louder than talking.")
        c1, c2 = st.columns(2)
        with c1:
            duration  = st.selectbox("How long:", ["15–30 minutes","1–2 hours","Half a day","Since yesterday","2–3 days","I can't remember her last words"])
            last_said = st.text_input("Last thing she said:", placeholder='"Fine." / "Okay." / [nothing]')
        with c2:
            trigger = st.text_area("What happened before?", height=100,
                          placeholder="e.g. Said I was watching cricket instead of helping with groceries")
        section_label("Describe the silence")
        silence_clues = st.multiselect("Select all that apply:", [
            "Same room, zero words","Moved to another room","One-word texts only",
            "Read receipts, no reply","Talking to everyone else normally",
            "She cried at some point","Polite but cold","Busy on phone but not with me",
        ])
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            decode_sil = st.button("Decode the silence →", use_container_width=True)
        if decode_sil:
            with st.spinner("Amplifying the silence..."):
                sp = (
                    "You are a silence analyst for " + rel_type.lower() + " communication — "
                    "where nothing is said but everything is communicated.\n\n"
                    "### 🔕 Silence Type\nName it: Processing / Hurt / Punishing / Testing / Exhausted / Other.\n\n"
                    "### 💭 What's Happening In Her Head\nSpecific and accurate — funny because it's true.\n\n"
                    "### ⏱️ The Duration Factor\nWhat " + duration + " of silence specifically signals.\n\n"
                    "### 🔍 The Real Issue\nOften not the surface trigger. What is this actually about?\n\n"
                    "### ☢️ Threat Level\n🟢 Needs space / 🟡 Needs acknowledgement / 🔴 Needs conversation / ☢️ Emergency\n\n"
                    "### 🛠️ Operation: Break The Silence\nStep-by-step. What to do, say, and NOT say.\n\n"
                    "### 💀 Worst Things To Say Right Now\n3 phrases that will make this worse. (These are probably the ones you want to say.)"
                )
                prompt = "Duration: " + duration + "\nLast words: " + last_said + "\nTrigger: " + trigger + "\nClues: " + (", ".join(silence_clues) or "Not specified")
                result = ask_claude(sp, prompt, 1200)
                save_history("😶 Silence Decoder", trigger or duration, result)
            show_result(result)

# ══════════════════════════════════════════
# SERIOUS FEATURES
# ══════════════════════════════════════════
else:

    if page == "🙏 Apology Workshop":
        page_header("Apology Workshop", "A good apology is a skill. Most people do it wrong.")
        callout(
            "A real apology has three parts: acknowledgement of what you did, "
            "understanding of its impact on her, and a genuine commitment to change.", "info"
        )
        what_happened = st.text_area("What happened? (be honest with yourself first)", height=110,
            placeholder="Describe what you did — not your justification, just what happened.")
        her_reaction  = st.text_input("How has " + rel_label + " responded?",
            placeholder="e.g. She went quiet / She said she was hurt / She told me directly")
        c1, c2 = st.columns(2)
        with c1:
            severity = st.selectbox("How significant was this?", [
                "Minor — a slip or oversight","Moderate — caused real hurt",
                "Significant — broke trust or a commitment","Serious — this has happened before",
            ])
        with c2:
            apology_style = st.selectbox("Delivery:", [
                "Spoken, face to face","Written note or card","Text message","Long heartfelt letter",
            ])
        apology_given = st.checkbox("I've already tried to apologise (didn't land well)")
        apology_how   = ""
        if apology_given:
            apology_how = st.text_input("What did you say?", placeholder="e.g. Said 'I'm sorry you felt that way'")
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            build = st.button("Build my apology →", use_container_width=True)
        if build:
            if not validate(what_happened, "What happened"): st.stop()
            with st.spinner("Working through this carefully..."):
                apology_note = ("\nPrevious attempt: " + apology_how) if apology_given and apology_how else ""
                sp = (
                    "You are a relationship counsellor helping craft a genuine apology to a "
                    + rel_type.lower() + " (" + rel_label + "), together " + str(years) + " years.\n\n"
                    "Goal: a REAL apology — genuine accountability, not conflict avoidance.\n\n"
                    "### What She Needs To Hear\nNot what he wants to say — what she needs to receive emotionally.\n\n"
                    "### The Apology\nWrite the full apology in " + apology_style + " format.\n"
                    "Make it specific, impact-focused, free of 'but' and 'if you felt' qualifiers, and natural.\n\n"
                    "### Why This Works\nWhat elements of a genuine apology this contains.\n\n"
                    "### What To Do Alongside It\n2–3 concrete actions that show the apology is real.\n\n"
                    "### Phrases That Undermine Apologies\n4–5 things NOT to say — brief note on why each backfires.\n\n"
                    "### Realistic Expectations\nHonest note on recovery given: " + severity + "."
                )
                result = ask_claude(sp, "What happened: " + what_happened + "\nHer response: " + her_reaction + "\nSeverity: " + severity + apology_note, 1500)
                save_history("🙏 Apology Workshop", what_happened[:80], result)
            show_result(result)

    elif page == "⚖️ Argument Referee":
        page_header("Argument Referee", "A neutral outside perspective. The verdict might not go your way.")
        callout("True neutrality means you might not like the answer. That's the point.", "warning")
        topic = st.text_input("What is the argument about?",
            placeholder="e.g. Division of household tasks / How we spend weekends / Something specific that was said")
        c1, c2 = st.columns(2)
        with c1:
            section_label("Your position")
            your_side = st.text_area("What you said / believe:", height=130, key="ys",
                placeholder="Your side — as honestly as you can manage.")
        with c2:
            section_label(rel_label.capitalize() + "'s position")
            her_side = st.text_area("What she said / believes:", height=130, key="hs",
                placeholder="Her side — try to represent it fairly.")
        how_long_arg = st.selectbox("How long has this been an issue?",
            ["First time","Come up before","Recurring pattern","Ongoing for a long time"])
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            ref = st.button("Get a fair reading →", use_container_width=True)
        if ref:
            if not validate(topic, "The topic"): st.stop()
            with st.spinner("Reading both sides carefully..."):
                sp = (
                    "You are a fair, thoughtful relationship mediator. Genuine neutrality — "
                    "not to make either person feel better, but to help them understand.\n\n"
                    "### What This Argument Is Really About\nThe underlying dynamic beneath the surface topic.\n\n"
                    "### What's Valid — His Side\nSpecific points where his position has genuine merit.\n\n"
                    "### What's Valid — Her Side\nSpecific points where her position has genuine merit.\n\n"
                    "### The Honest Verdict\nWho has the stronger argument and why. Be direct.\n\n"
                    "### What's Fuelling The Conflict\nBehaviours on BOTH sides making this harder.\n\n"
                    "### A Path Forward\nSpecific, actionable steps to resolve THIS argument.\n\n"
                    "### The Bigger Picture\nIf recurring: what does this point to?"
                )
                result = ask_claude(sp, "Topic: " + topic + "\nHis position: " + your_side + "\nHer position: " + her_side + "\nPattern: " + how_long_arg, 1400)
                save_history("⚖️ Argument Referee", topic, result)
            show_result(result)

    elif page == "🎁 Gift Advisor":
        page_header("Gift Advisor", "The best gifts show you were paying attention.")
        c1, c2 = st.columns(2)
        with c1:
            occasion = st.selectbox("Occasion:", [
                "Apology / Making it right","Anniversary","Birthday",
                "Just because — no occasion","She's had a hard time lately",
                "Celebrating something she achieved","Reconnecting after distance",
            ])
            budget = st.selectbox("Budget:", ["Under $50","$50–150","$150–300","$300–500","$500+"])
        with c2:
            her_interests  = st.text_input("Her interests / things she loves:",
                placeholder="e.g. cooking, reading, plants, long baths, a specific author")
            recent_context = st.text_area("Anything relevant lately?", height=88,
                placeholder="e.g. She mentioned wanting to learn something / stressed at work / gave something up")
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            gift = st.button("Get thoughtful ideas →", use_container_width=True)
        if gift:
            with st.spinner("Thinking this through..."):
                sp = (
                    "You are a thoughtful gift advisor for a " + rel_type.lower()
                    + " (" + rel_label + "), " + str(years) + " years together.\n\n"
                    "Best gifts: specific, personal, show attention. Avoid generic.\n\n"
                    "### What This Occasion Calls For\nWhat kind of gift energy fits — and why.\n\n"
                    "### Three Considered Recommendations\n"
                    "For each: what it is, why it fits HER specifically, how to present it, realistic cost.\n\n"
                    "### The Thoughtful Detail\nOne small, low-cost addition that shows real attention.\n\n"
                    "### What To Avoid\n2–3 gift types that would miss the mark.\n\n"
                    "### A Note on Presentation\nHow to give it — timing, what to say.\n\n"
                    "Goal: a gift that says 'I know you', not 'I got you something'."
                )
                result = ask_claude(sp, "Occasion: " + occasion + "\nBudget: " + budget + "\nInterests: " + her_interests + "\nContext: " + recent_context, 1300)
                save_history("🎁 Gift Advisor", occasion + " / " + budget, result)
            show_result(result)

    elif page == "📅 Date Planner":
        page_header("Date Planner", "Worth planning well. The effort shows.")
        c1, c2 = st.columns(2)
        with c1:
            rel_state = st.selectbox("How are things between you right now?", [
                "Good — this is a treat","Neutral — need some quality time",
                "A bit distant — need to reconnect","After a rough patch — a fresh start",
            ])
            location = st.text_input("Your city:", placeholder="e.g. Sydney")
        with c2:
            budget_date = st.selectbox("Budget:", ["Under $50","$50–150","$150–300","$300+"])
            constraints = st.multiselect("Constraints:", [
                "Have kids / babysitter needed","Weeknight only","Daytime only",
                "She hates loud / crowded places","Outdoors preferred","She's stressed — needs low-key",
            ])
        her_prefs = st.text_input("What does she enjoy?",
            placeholder="e.g. good food, walks, trying new things, quiet evenings, live music")
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            plan = st.button("Plan a good date →", use_container_width=True)
        if plan:
            with st.spinner("Planning something worth the effort..."):
                sp = (
                    "Help plan a genuinely good date — " + rel_type.lower() + ", "
                    + str(years) + " years, in " + (location or "Sydney, Australia") + ".\n\n"
                    "Current state: " + rel_state + ". Tailor the date TYPE to match.\n\n"
                    "### The Right Kind of Date for Right Now\nWhat KIND of experience will land — and why.\n\n"
                    "### A Considered Plan\nReal itinerary — specific venue types, vibe, area. "
                    "How to invite her. Rough timing. 2–3 moments that create genuine connection.\n\n"
                    "### The Detail That Makes It\nOne specific thing that elevates it from nice to memorable.\n\n"
                    "### What To Avoid\nBased on her preferences and current state.\n\n"
                    "### Budget Guide\nHow to spend it well.\n\n"
                    "Goal: genuine connection, not just a nice outing."
                )
                result = ask_claude(sp, "State: " + rel_state + "\nBudget: " + budget_date + "\nConstraints: " + (", ".join(constraints) or "None") + "\nPreferences: " + her_prefs, 1300)
                save_history("📅 Date Planner", rel_state, result)
            show_result(result)

    elif page == "🌡️ Relationship Check-in":
        page_header("Relationship Check-in", "Worth doing when things are good — not just when they're not.")
        q1 = st.slider("Arguments / friction in the last month  (0 = none, 10 = a lot):", 0, 10, 2)
        q2 = st.slider("How well are you communicating right now?  (1 = poorly, 10 = very well):", 1, 10, 6)
        q3 = st.slider("How connected do you feel right now?  (1–10):", 1, 10, 6)
        q4 = st.slider("How satisfied do you think SHE is right now?  (1–10):", 1, 10, 6)
        q5 = st.slider("How satisfied are YOU right now?  (1–10):", 1, 10, 7)
        c1, c2 = st.columns(2)
        with c1:
            quality_time = st.selectbox("Quality time together lately:", ["None","Very little","Some","A good amount"])
            affection    = st.selectbox("Affection levels:", ["Very low","Low","Normal","High"])
        with c2:
            going_well = st.text_input("What's genuinely going well:", placeholder="e.g. We laugh a lot / Good teamwork with the kids")
            needs_work = st.text_input("What needs more attention:", placeholder="e.g. Not much time alone / I've been distracted")
        _, cc, _ = st.columns([1, 2, 1])
        with cc:
            checkin = st.button("Get an honest read →", use_container_width=True)
        if checkin:
            with st.spinner("Reading the full picture..."):
                score = round((q2 + q3 + q4 + q5) / 4 - (q1 * 0.25), 1)
                sp = (
                    "You are a thoughtful relationship counsellor. Honest, constructive — "
                    "not alarmist, not falsely reassuring.\n\n"
                    "### Where Things Are Right Now\nOne honest paragraph — positive and concerning.\n\n"
                    "### What's Working\nSpecific strengths. Not generic.\n\n"
                    "### What Needs Attention\n1–3 specific areas with context for why each matters.\n\n"
                    "### One Thing This Week\nThe single highest-leverage thing they could do in 7 days. Specific and achievable.\n\n"
                    "### A Longer View\nIf current patterns continue — where does this go in 6 months? Be honest.\n\n"
                    "### A Note\nOne warm, direct observation about this couple.\n\n"
                    "Tone: trusted friend with real perspective."
                )
                prompt = (
                    "Friction: " + str(q1) + "/10, Communication: " + str(q2) + "/10, "
                    "Connection: " + str(q3) + "/10\nHer satisfaction: " + str(q4)
                    + "/10, My satisfaction: " + str(q5) + "/10\nQuality time: "
                    + quality_time + ", Affection: " + affection
                    + "\nGoing well: " + (going_well or "Not mentioned")
                    + "\nNeeds work: " + (needs_work or "Not mentioned")
                )
                result = ask_claude(sp, prompt, 1400)
                save_history("🌡️ Relationship Check-in", "Score ~" + str(score) + "/10", result)
            st.metric("Indicative score", str(score) + " / 10",
                help="Based on your inputs — not a scientific measurement.")
            show_result(result)

# ══════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════
if page == "🕑 History":
    page_header("History", str(len(st.session_state.history)) + " reading(s) this session.")
    if not st.session_state.history:
        callout("Nothing yet. Use any feature and your results will appear here.", "tip")
    else:
        c1, _, _ = st.columns([1, 1, 3])
        with c1:
            if st.button("Clear all", use_container_width=True):
                st.session_state.history      = []
                st.session_state.phrase_result  = None
                st.session_state.phrase_current = None
                st.rerun()
        fdivider()
        for item in st.session_state.history:
            tag = "😂" if item.get("mode") == "comedy" else "🧠"
            label = tag + "  " + item["feature"] + "  ·  " + item["time"] + "  ·  \"" + item["input"] + "\""
            with st.expander(label):
                st.markdown(item["result"])
