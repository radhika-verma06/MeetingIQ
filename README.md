# 🎙️ MeetingIQ

Private, user-controlled meeting intelligence for sensitive conversations.

🚀 **Live Demo:** https://meetingiq-afgqc4x7yvtnswncjsvqlu.streamlit.app/

MeetingIQ turns raw meeting transcripts or recordings into structured, actionable reports: summaries, owners, deadlines, key decisions, sentiment, topics, charts, and exports.

> **Killer use case:** MeetingIQ is for the meetings you would not feel comfortable uploading to a black-box free summarizer.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-BYOK-green?logo=openai)](https://openai.com/)
[![Local LLM](https://img.shields.io/badge/Local%20LLM-Ollama-purple)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Why use MeetingIQ instead of free meeting tools?

Free tools are convenient. MeetingIQ is built for control.

| Need | Free meeting tools | MeetingIQ |
|---|---|---|
| Instant hosted convenience | ✅ Usually | ✅ Demo Mode available |
| Analyze confidential meetings | ⚠️ Requires trusting vendor retention policies | ✅ User-controlled backend |
| Bring your own OpenAI key | ❌ Usually no | ✅ Yes |
| Local AI option | ❌ Rare | ✅ Ollama support |
| Open-source/auditable code | ❌ Usually no | ✅ Yes |
| Customizable prompts and pipeline | ⚠️ Limited | ✅ Edit the code/prompt directly |
| Structured decisions/action items | ⚠️ Sometimes | ✅ First-class output |
| Export machine-readable data | ⚠️ Limited | ✅ Markdown + JSON |

**Positioning:** MeetingIQ does not try to beat every free tool on convenience. It gives privacy-conscious users and teams a transparent meeting-analysis layer they can run with Demo Mode, OpenAI BYOK, or local Ollama.

---

## 🎬 Demo video and screenshots

- Demo video: [`assets/meetingiq-demo.mp4`](assets/meetingiq-demo.mp4)
- Home screen: [`assets/meetingiq-home.png`](assets/meetingiq-home.png)
- Sample loaded: [`assets/meetingiq-sample-loaded.png`](assets/meetingiq-sample-loaded.png)
- Results screen: [`assets/meetingiq-results.png`](assets/meetingiq-results.png)

---

## ✨ Features

- 📝 Executive meeting summaries
- ✅ Action items with owner and deadline extraction
- 🏛️ Key decision capture
- 💬 Sentiment and tone analysis
- 📊 Visual insights with Plotly charts
- 🎙️ Audio transcription through OpenAI Whisper
- 🧪 Demo Mode for no-key testing with sample data
- 🔐 User-controlled AI backend: OpenAI BYOK or local Ollama
- 📤 One-click Markdown and JSON export
- 🐳 Docker-ready deployment

---

## 🧭 Best-fit use cases

MeetingIQ is especially useful for conversations where data control matters:

- startup strategy meetings
- student organization planning
- product standups
- research interviews
- HR/internal notes
- board or leadership meetings
- legal, medical, academic, or privacy-sensitive discussions

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| App/UI | Streamlit + custom CSS |
| Cloud AI | OpenAI GPT-4o using the user's own API key |
| Local AI | Ollama-compatible local models |
| Audio transcription | OpenAI Whisper API |
| Visualization | Plotly |
| Language | Python 3.10+ |
| Packaging | pip, Docker |

---

## ⚙️ How It Works

```text
Transcript or Audio Upload
        │
        ▼
Transcript Parser / Audio Transcription
        │
        ▼
AI Backend Selection
  ├── Demo Mode mock data
  ├── OpenAI BYOK cloud analysis
  └── Ollama local analysis
        │
        ▼
Structured JSON Output
        │
        ▼
Summary + Actions + Decisions + Sentiment + Charts
        │
        ▼
Markdown / JSON Export
```

Key engineering choices:

- Single-pass structured extraction to reduce latency
- JSON-first prompting to make results easier to render and export
- Local-model option for privacy-sensitive workflows
- Demo Mode so evaluators can try the app without creating an account or pasting an API key

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.10+
- Optional: [OpenAI API key](https://platform.openai.com/api-keys) for cloud analysis and audio transcription
- Optional: [Ollama](https://ollama.com/) for local LLM analysis

### 1. Clone the repository

```bash
git clone https://github.com/radhika-verma06/MeetingIQ.git
cd MeetingIQ
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment (optional)

```bash
cp .env.example .env
# Edit .env and add your OpenAI key if you want cloud analysis/audio transcription
```

### 5. Run the app

```bash
streamlit run app.py
```

The app opens at http://localhost:8501.

### Docker deployment

```bash
docker build -t meetingiq .
docker run -p 8501:8501 meetingiq
```

---

## 🧪 How to try it quickly

1. Open the live demo.
2. Keep **Demo Mode** enabled.
3. Click **Load sample transcript**.
4. Click **Analyze Meeting**.
5. Review the summary, action items, decisions, sentiment, charts, and exports.

No OpenAI key is needed for Demo Mode.

### Auditable smoke test

Judges or reviewers can verify the demo pipeline locally:

```bash
python tools/demo_smoke.py
```

This checks the built-in demo transcript, mock analysis output, and chart-rendering functions.

---

## 🔐 Privacy model

MeetingIQ supports multiple privacy levels:

- **Demo Mode:** uses built-in sample/mock data; no key required.
- **OpenAI BYOK:** the user provides their own OpenAI API key. Transcript/audio data is sent to OpenAI for processing.
- **Ollama Local:** meeting transcript analysis can run against a local Ollama model on the user's machine.

MeetingIQ itself does not intentionally store user API keys or transcripts to disk. Users should still choose the backend that matches the sensitivity of their meeting.

---

## 📁 Project Structure

```text
MeetingIQ/
├── app.py                    # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── audio_processor.py    # Whisper transcription helper
│   ├── charts.py             # Plotly chart builders
│   ├── llm_client.py         # OpenAI/Ollama integrations
│   └── parser.py             # Transcript preprocessing utilities
├── .github/workflows/ci.yml  # Smoke-test CI
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## ⚠️ Current Limitations

- OpenAI mode sends transcript text to OpenAI's API.
- Audio transcription currently uses OpenAI Whisper unless Demo Mode is enabled.
- Ollama mode requires Ollama running locally with a pulled model.
- Speaker diarization is not yet implemented.
- Calendar/Slack/Notion integrations are planned but not yet built.

---

## 🔮 Future Improvements

- Speaker diarization and per-speaker sentiment
- Multi-language transcript analysis
- Calendar/Notion task export
- Historical dashboard for meeting trends
- Custom templates for standups, sales calls, research interviews, and board meetings
- Fully local audio transcription option

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

Built as a demonstration of production-grade, privacy-aware LLM application development.
