# 💑 She Said What? — v2

> Two apps in one. Switch between **😂 Comedy Mode** (for laughs) and **🧠 Serious Mode** (for moments that actually matter) with a single button.

---

## What Is This?

A Streamlit app powered by Claude AI that helps navigate relationship communication — with a clear purpose split:

| Mode | Purpose | Features |
|------|---------|----------|
| 😂 **Comedy** | Relatable humour about communication patterns | What She Really Said · Phrase Bible · Danger Meter · Emoji Translator · Silence Decoder |
| 🧠 **Serious** | Genuine tools for real moments | Apology Workshop · Argument Referee · Gift Advisor · Date Planner · Relationship Check-in |

The toggle is in the sidebar. Switching modes changes the entire visual theme and feature set instantly.

---

## Prerequisites

- Python **3.9+**
- An **Anthropic API key** — get one at [console.anthropic.com](https://console.anthropic.com)
- Internet connection (for API calls + Google Fonts)

---

## Installation

```bash
# 1. Place files in a folder
cd she-said-what

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate       # macOS / Linux
# venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Running

**macOS / Linux:**
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
streamlit run app.py
```

**Windows Command Prompt:**
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
streamlit run app.py
```

**One-liner:**
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here streamlit run app.py
```

Opens at **http://localhost:8501**

---

## Streamlit Cloud Deployment

1. Push these three files to GitHub:
   ```
   app.py
   requirements.txt
   README.md
   ```
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Set key: **Manage app → Settings → Secrets**
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
4. Deploy.

> ⚠️ Never commit your API key to git.

---

## Project Structure

```
she-said-what/
├── app.py              # Entire app (single file, 1200 lines)
├── requirements.txt    # streamlit + anthropic
└── README.md
```

---

## Feature Reference

### 😂 Comedy Mode

| Feature | What it does |
|---------|-------------|
| 💬 What She Really Said | Decodes any message — threat level, mission briefing, magic words to say |
| 📖 The Phrase Bible | 18 classic phrases decoded on click + custom lookup |
| 🚨 Danger Meter | Situation assessment with danger score and survival probability % |
| 🔢 Emoji Translator | Decodes any emoji sequence in context |
| 😶 Silence Decoder | Classifies silence type + step-by-step break-the-silence guide |

### 🧠 Serious Mode

| Feature | What it does |
|---------|-------------|
| 🙏 Apology Workshop | Full genuine apology — specific to what happened, action plan, phrases to never say |
| ⚖️ Argument Referee | Neutral verdict on who's right, the real underlying issue, resolution path |
| 🎁 Gift Advisor | Thoughtful gift ideas based on occasion, her interests, and recent context |
| 📅 Date Planner | Full itinerary matched to your relationship state, budget, and her preferences |
| 🌡️ Relationship Check-in | 5-slider health check with honest assessment and action plan |

---

## Sidebar — Personalise First

Fill in before using any feature:
- **Her name / nickname** — personalises every prompt
- **Your name** — included in context
- **Relationship type** — Wife / Girlfriend / Fiancée / Partner
- **Years together** — affects tone and advice depth

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ANTHROPIC_API_KEY not set` | Set env variable before running — see above |
| Authentication error (in-app) | Key invalid — generate new one at console.anthropic.com |
| Rate limit hit | Wait 30–60 seconds, retry |
| Text hard to read | `pip install --upgrade streamlit` |
| Fonts not loading | Restricted network — app still works with system fonts |

---

## Notes

- Comedy Mode is for entertainment. Serious Mode prompts are designed for genuine use.
- Conversations are sent to Anthropic's API. Don't enter sensitive personal information.
- Session history resets on browser refresh — not persisted between sessions.
- Model: `claude-sonnet-4-5`

---

*Built with [Streamlit](https://streamlit.io) + [Anthropic Claude](https://anthropic.com)*
