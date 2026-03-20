# 🎙️ MeetingIQ —An AI-powered meeting intelligence system that turns raw transcripts into professional, actionable reports.

🚀 **Live Demo**: [meetingiq.streamlit.app](https://meetingiq-afgqc4x7yvtnswncjsvqlu.streamlit.app/)
> Transform raw meeting transcripts into structured, actionable intelligence — powered by GPT-4o.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green?logo=openai)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

**MeetingIQ** is a production-grade AI application that takes any meeting transcript and runs it through a structured LLM pipeline to produce:

- ✅ Executive summaries
- ✅ Extracted action items with owner & deadline attribution
- ✅ Key decisions captured and catalogued
- ✅ Sentiment & tone analysis
- ✅ Visual insights via interactive Plotly charts
- ✅ One-click export to Markdown and JSON

Built with a SaaS-grade dark UI in Streamlit, this project demonstrates real-world LLM integration, prompt engineering, and data visualization.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📝 Smart Summarization | 3–5 sentence executive summary distilled from any length transcript |
| 🎙️ Audio Transcription | Upload .mp3/.wav files for automatic Whisper AI transcription |
| ✅ Action Item Extraction | Tasks with owner and deadline parsed from natural language |
| 🏛️ Decision Capture | Structured list of key decisions made during the meeting |
| 📊 Visual Insights | Owner breakdown bar chart + topic distribution donut chart |
| 📤 Export | Download results as `.md` or `.json` |
| 🛡️ Production Ready | Dockerized, adaptive theming, and multi-format support |

---

## 💎 Why MeetingIQ?

While other free transcriptors exist, MeetingIQ is designed for **Decision Makers**, not just data collection. 

| Capability | Raw Transcriptors | **MeetingIQ** |
| :--- | :---: | :---: |
| **Transcription AI** | ✅ | ✅ |
| **Reasoning LLM (GPT-4o/Llama3)** | ❌ | **✅** |
| **Action Item Extraction** | ❌ | **✅** |
| **Emotional Sentiment Analysis** | ❌ | **✅** |
| **Zero-API Local Inference** | ⚠️ (Technical) | **✅ (Visual/Easy)** |
| **Data Sovereignty** | ⚠️ (Cloud base) | **💎 100% Local** |

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit, custom CSS (dark theme) |
| LLM | OpenAI GPT-4o (JSON mode) |
| Visualization | Plotly (gauge, bar, pie charts) |
| Language | Python 3.10+ |
| Packaging | pip, requirements.txt |

---

## ⚙️ How It Works

```
User Input (text/file)
        │
        ▼
   Pre-Processing        ← parser.py: clean, detect speakers, estimate duration
        │
        ▼
   LLM Inference         ← llm_client.py: structured JSON prompt → OpenAI API
        │
        ▼
   Response Parsing      ← Safe JSON deserialization with fallback handling
        │
        ▼
   Visualization Layer   ← charts.py: Plotly gauge + bar + donut charts
        │
        ▼
   Streamlit Display     ← Tabbed UI: Summary / Actions / Decisions / Sentiment
        │
        ▼
   Export                ← .md and .json download buttons
```

**Key prompt engineering decisions:**
- Single-pass JSON extraction for all sections (reduces latency vs. multi-call approaches)
- `temperature=0.2` for highly factual, consistent outputs
- GPT-4o JSON mode (`response_format: {type: "json_object"}`) eliminates markdown fence hallucinations
- Dynamic schema prompt — only requests sections the user has toggled on

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/meetingiq.git
cd meetingiq
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
# Edit .env and add your OPENAI_API_KEY
```

### 5. Run the app
```bash
streamlit run app.py
```

### ⚡ Docker Deployment (Production)
```bash
docker build -t meetingiq .
docker run -p 8501:8501 meetingiq
```

The app will open at `http://localhost:8501`

### 6. Enter your API key
Enter your OpenAI API key in the **sidebar** (never stored to disk).

---

## 📁 Project Structure

```
meetingiq/
├── app.py                    # Main Streamlit application
├── utils/
│   ├── __init__.py
│   ├── llm_client.py         # OpenAI API integration & prompt engineering
│   ├── parser.py             # Transcript pre-processing utilities
│   └── charts.py             # Plotly chart builders
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔮 Future Improvements

- [ ] **Speaker diarization** — Attribute sentiment per speaker
- [ ] **Multi-language support** — Auto-detect and translate transcripts
- [ ] **Calendar integration** — Push action items directly to Google Calendar / Notion
- [ ] **Audio input** — Accept `.mp3`/`.mp4` via Whisper transcription pipeline
- [ ] **Historical dashboard** — Track meeting health metrics over time
- [ ] **Team collaboration** — Share reports via Slack / email integration
- [ ] **Custom templates** — Sales calls, standups, board meetings have different extraction needs

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built as a demonstration of production-grade LLM application development.*
