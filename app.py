"""
AI Meeting Intelligence System
================================
A production-grade Streamlit app that analyzes meeting transcripts using LLMs.
Provides summaries, action items, decisions, and sentiment analysis.
"""

import streamlit as st
import time
import os
from utils.llm_client import analyze_transcript, analyze_transcript_ollama, get_mock_analysis
from utils.parser import extract_sections
from utils.audio_processor import transcribe_audio, get_mock_transcription
from utils.charts import (
    render_sentiment_gauge,
    render_action_item_chart,
    render_topic_distribution,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MeetingIQ · AI Meeting Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — polished SaaS aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-overall: #f1f0fb;
        --glass-bg: rgba(255, 255, 255, 0.95);
        --glass-border: rgba(167, 139, 250, 0.4);
        --text-main: #020617;
        --text-muted: #4338ca;
        --accent: #6d28d9;
        --accent-glow: rgba(167, 139, 250, 0.3);
        --success: #059669;
        --hero-gradient: linear-gradient(135deg, #ddd6fe 0%, #c4b5fd 100%);
        --card-shadow: 0 10px 40px -10px rgba(167, 139, 250, 0.2);
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --bg-overall: #030014;
            --glass-bg: rgba(15, 12, 41, 0.7);
            --glass-border: rgba(139, 92, 246, 0.3);
            --text-main: #f5f3ff;
            --text-muted: #a78bfa;
            --accent: #c4b5fd;
            --accent-glow: rgba(139, 92, 246, 0.2);
            --success: #34d399;
            --hero-gradient: linear-gradient(135deg, #1e1b4b 0%, #2e1065 100%);
            --card-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.5);
        }
    }

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Layout & Background */
    .stApp {
        background-color: var(--bg-overall);
        background-image: 
            radial-gradient(at 0% 0%, var(--accent-glow) 0px, transparent 50%),
            radial-gradient(at 100% 100%, var(--accent-glow) 0px, transparent 50%);
        color: var(--text-main);
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-right: 1px solid var(--glass-border);
    }

    /* Glass Card Base */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 1.75rem;
        box-shadow: var(--card-shadow);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid var(--accent);
        box-shadow: 0 12px 40px -4px rgba(0, 0, 0, 0.1);
    }

    /* Hero header */
    .hero-header {
        background: var(--hero-gradient);
        border-radius: 28px;
        padding: 3.5rem 2.5rem;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .hero-header::after {
        content: "";
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle at center, var(--accent-glow) 0%, transparent 40%);
        opacity: 0.5;
        pointer-events: none;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.04em;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: rgba(255, 255, 255, 0.65);
        margin-top: 0.6rem;
        font-weight: 400;
    }

    /* Metrics with Glow */
    .metric-card {
        background: var(--glass-bg);
        backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid var(--glass-border);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: var(--accent);
        box-shadow: 0 0 20px var(--accent-glow);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--accent);
        letter-spacing: -0.02em;
    }
    .metric-label {
        font-size: 0.825rem;
        color: var(--text-muted);
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.1em;
        margin-top: 0.4rem;
    }

    /* Custom Input Areas */
    .stTextArea textarea {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px !important;
        color: var(--text-main) !important;
        padding: 1rem !important;
        transition: border-color 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-glow) !important;
    }

    /* Premium Buttons */
    .stButton > button {
        background: var(--accent) !important;
        color: white !important;
        border-radius: 14px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton > button:hover {
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 10px 25px -5px var(--accent-glow) !important;
    }

    /* Status Badges */
    .sentiment-positive { background: rgba(16, 185, 129, 0.15); color: var(--success); padding: 6px 14px; border-radius: 12px; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.2); }
    .sentiment-negative { background: rgba(239, 68, 68, 0.15); color: #f87171; padding: 6px 14px; border-radius: 12px; font-weight: 700; border: 1px solid rgba(239, 68, 68, 0.2); }
    .sentiment-neutral { background: rgba(59, 130, 246, 0.15); color: var(--accent); padding: 6px 14px; border-radius: 12px; font-weight: 700; border: 1px solid rgba(59, 130, 246, 0.2); }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--glass-bg);
        border-radius: 16px;
        padding: 6px;
        border: 1px solid var(--glass-border);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 16px;
        color: var(--text-muted);
        transition: all 0.2s ease;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--accent) !important;
        color: #ffffff !important;
    }

    /* Hide standard Streamlit clutter */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")

    model_source = st.radio(
        "Model Provider",
        ["OpenAI (Cloud)", "Ollama (Local)"],
        index=0,
        help="Choose between OpenAI Cloud or a Local Ollama instance (no API key required)."
    )

    st.markdown("---")

    if model_source == "OpenAI (Cloud)":
        # API key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Your OpenAI API key. Keys are never stored.",
        )

        model_choice = st.selectbox(
            "Model",
            ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            index=0,
            help="GPT-4o recommended for best analysis quality.",
        )
    else:
        api_key = "" # Not needed for Ollama
        model_choice = st.text_input(
            "Ollama Model Name",
            value="llama3",
            help="The name of the model you have pulled in Ollama (e.g., llama3, mistral, phi3)."
        )

    st.markdown("---")
    st.markdown("### 📋 Analysis Options")

    demo_mode = st.toggle(
        "✨ Demo Mode", 
        value=False, 
        help="Explore MeetingIQ without an OpenAI API key using high-quality mock data."
    )

    do_summary = st.toggle("Meeting Summary", value=True)
    do_actions = st.toggle("Action Items", value=True)
    do_decisions = st.toggle("Key Decisions", value=True)
    do_sentiment = st.toggle("Sentiment Analysis", value=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:var(--text-muted); line-height:1.6;'>
    <b style='color:var(--accent)'>MeetingIQ v1.1</b><br>
    Premium Analytics System<br>
    Zero-Log Data Privacy<br><br>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div style="display:flex; align-items:center; gap:1rem;">
        <div style="font-size:2.8rem;">🎙️</div>
        <div>
            <div class="hero-title">MeetingIQ</div>
            <div class="hero-subtitle">Turn any meeting transcript into actionable intelligence — instantly.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────────────
input_col, _ = st.columns([3, 1])
with input_col:
    st.markdown("#### 📄 Input Transcript")

    input_method = st.radio(
        "Input method",
        ["Paste Text", "Upload Text File", "Upload Audio Recording"],
        horizontal=True,
        label_visibility="collapsed",
    )

    transcript_text = ""

    if input_method == "Paste Text":
        transcript_text = st.text_area(
            "Paste meeting transcript here",
            height=220,
            placeholder=(
                "Example:\n\n"
                "Sarah: Good morning everyone. Let's start the Q3 planning review.\n"
                "John: Thanks Sarah. We need to finalize the product roadmap by Friday.\n"
                "Lisa: Agreed. I'll handle the design mockups. Can we get engineering estimates?\n"
                "John: I'll coordinate with the backend team and send estimates by Wednesday.\n"
                "Sarah: Perfect. Decision made — we ship feature X in Q3, feature Y moves to Q4.\n"
                "Lisa: I'm concerned about the timeline. We might be overcommitting.\n"
                "John: Good point. Let's add a buffer week. I'll update the roadmap.\n"
            ),
            label_visibility="collapsed",
        )
    elif input_method == "Upload Text File":
        uploaded_file = st.file_uploader(
            "Upload transcript (.txt or .md)",
            type=["txt", "md"],
            label_visibility="collapsed",
        )
        if uploaded_file:
            transcript_text = uploaded_file.read().decode("utf-8")
            st.success(f"✅ File loaded: **{uploaded_file.name}** ({len(transcript_text):,} characters)")
            with st.expander("Preview transcript"):
                st.text(transcript_text[:1500] + ("..." if len(transcript_text) > 1500 else ""))
    else:
        audio_file = st.file_uploader(
            "Upload meeting recording (.mp3, .wav, .m4a)",
            type=["mp3", "wav", "m4a"],
            label_visibility="collapsed",
        )
        if audio_file:
            st.info("🎵 Audio file ready for transcription.")
            st.session_state["audio_file"] = audio_file

    st.markdown("")
    analyze_btn = st.button("🔍 Analyze Meeting", use_container_width=True)


# ─────────────────────────────────────────────
# ANALYSIS ENGINE
# ─────────────────────────────────────────────
if analyze_btn:
    if input_method == "Upload Audio Recording":
        if "audio_file" not in st.session_state:
            st.warning("⚠️ Please upload an audio recording first.")
            st.stop()
    elif not transcript_text.strip():
        st.warning("⚠️ Please provide a meeting transcript or recording.")
        st.stop()

    if not demo_mode and not api_key.strip():
        st.warning("⚠️ Please enter your OpenAI API key in the sidebar or enable Demo Mode.")
        st.stop()

    # Progress indicator
    with st.status("🧠 Processing meeting data...", expanded=True) as status:
        # Transcription Step
        if input_method == "Upload Audio Recording":
            st.write("🎙️ Transcribing audio using Whisper...")
            if demo_mode:
                time.sleep(2.0)
                transcript_text = get_mock_transcription()
            else:
                # Save temp file
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(st.session_state["audio_file"].name)[1]) as tmp:
                    tmp.write(st.session_state["audio_file"].getvalue())
                    tmp_path = tmp.name
                
                try:
                    transcript_text = transcribe_audio(tmp_path, api_key)
                finally:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
            
            st.success("✅ Transcription complete!")
            st.session_state["transcript"] = transcript_text

        st.write("Extracting semantic structure...")
        time.sleep(0.4)
        st.write("Running LLM inference pipeline...")

        if demo_mode:
            st.write("Fetching demo analysis...")
            time.sleep(1.2)
            results = get_mock_analysis()
        elif model_source == "Ollama (Local)":
            st.write(f"Running local inference ({model_choice})...")
            results = analyze_transcript_ollama(
                transcript=transcript_text,
                model=model_choice,
                do_summary=do_summary,
                do_actions=do_actions,
                do_decisions=do_decisions,
                do_sentiment=do_sentiment,
            )
        else:
            # Core LLM call — all prompts run together for efficiency
            results = analyze_transcript(
                transcript=transcript_text,
                api_key=api_key,
                model=model_choice,
                do_summary=do_summary,
                do_actions=do_actions,
                do_decisions=do_decisions,
                do_sentiment=do_sentiment,
            )

        st.write("Parsing and formatting results...")
        time.sleep(0.3)
        status.update(label="✅ Analysis complete!", state="complete")

    # Store in session state for persistence
    st.session_state["results"] = results
    st.session_state["transcript"] = transcript_text


# ─────────────────────────────────────────────
# RESULTS DISPLAY
# ─────────────────────────────────────────────
if "results" in st.session_state:
    results = st.session_state["results"]
    transcript = st.session_state["transcript"]

    st.markdown("---")

    # ── METRICS ROW ──────────────────────────
    word_count = len(transcript.split())
    speaker_lines = [l for l in transcript.split("\n") if ":" in l]
    estimated_speakers = len(set(
        line.split(":")[0].strip() for line in speaker_lines if line.strip()
    ))
    action_count = len(results.get("action_items", []))
    decision_count = len(results.get("decisions", []))

    m1, m2, m3, m4 = st.columns(4)
    for col, val, label in [
        (m1, f"{word_count:,}", "Words Analyzed"),
        (m2, str(max(estimated_speakers, 1)), "Participants"),
        (m3, str(action_count), "Action Items"),
        (m4, str(decision_count), "Key Decisions"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABBED RESULTS ────────────────────────
    tabs = st.tabs([
        "📝 Summary",
        "✅ Action Items",
        "🏛️ Decisions",
        "💬 Sentiment",
        "📊 Insights",
    ])

    # ── TAB 1: SUMMARY ────────────────────────
    with tabs[0]:
        st.markdown('<div class="section-title">MEETING SUMMARY</div>', unsafe_allow_html=True)
        if results.get("summary"):
            st.markdown(f"""
            <div class="glass-card">
                <p style="color:#cbd5e0; line-height:1.8; font-size:0.95rem; margin:0;">
                    {results["summary"]}
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Summary not requested or unavailable.")

        # Key topics
        if results.get("key_topics"):
            st.markdown('<div class="section-title" style="margin-top:1rem;">KEY TOPICS DISCUSSED</div>', unsafe_allow_html=True)
            topic_cols = st.columns(min(len(results["key_topics"]), 4))
            for i, topic in enumerate(results["key_topics"][:4]):
                with topic_cols[i % 4]:
                    st.markdown(f"""
                    <div style="background:#1a2535; border:1px solid #2d3748; border-radius:8px;
                                padding:0.6rem 1rem; text-align:center; color:#a0aec0;
                                font-size:0.85rem; font-weight:500;">
                        {topic}
                    </div>
                    """, unsafe_allow_html=True)

    # ── TAB 2: ACTION ITEMS ───────────────────
    with tabs[1]:
        st.markdown('<div class="section-title">ACTION ITEMS</div>', unsafe_allow_html=True)
        action_items = results.get("action_items", [])
        if action_items:
            for i, item in enumerate(action_items, 1):
                # item can be a string or dict with owner/deadline
                if isinstance(item, dict):
                    text = item.get("task", str(item))
                    owner = item.get("owner", "")
                    deadline = item.get("deadline", "")
                    meta = ""
                    if owner:
                        meta += f'<span style="color:#63b3ed; font-size:0.78rem;">👤 {owner}</span>'
                    if deadline:
                        meta += f'<span style="color:#68d391; font-size:0.78rem; margin-left:1rem;">📅 {deadline}</span>'
                    st.markdown(f"""
                    <div class="action-item">
                        <span class="action-bullet">#{i}</span>
                        <div>
                            <div class="action-text">{text}</div>
                            {"<div style='margin-top:4px;'>" + meta + "</div>" if meta else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="action-item">
                        <span class="action-bullet">#{i}</span>
                        <div class="action-text">{item}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No action items identified, or this analysis was not requested.")

    # ── TAB 3: DECISIONS ─────────────────────
    with tabs[2]:
        st.markdown('<div class="section-title">KEY DECISIONS MADE</div>', unsafe_allow_html=True)
        decisions = results.get("decisions", [])
        if decisions:
            for i, decision in enumerate(decisions, 1):
                st.markdown(f"""
                <div class="decision-item">
                    <span class="decision-bullet">✓</span>
                    <div class="decision-text">{decision}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No key decisions identified, or this analysis was not requested.")

    # ── TAB 4: SENTIMENT ─────────────────────
    with tabs[3]:
        sentiment_data = results.get("sentiment", {})
        if sentiment_data:
            s_col1, s_col2 = st.columns([1, 2])

            with s_col1:
                overall = sentiment_data.get("overall", "neutral").lower()
                badge_class = f"sentiment-{overall}"
                score = sentiment_data.get("score", 0.5)
                score_pct = int(score * 100)

                st.markdown('<div class="section-title">OVERALL SENTIMENT</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="section-card" style="text-align:center;">
                    <div style="font-size:3rem; margin-bottom:0.5rem;">
                        {"😊" if overall == "positive" else "😐" if overall == "neutral" else "😟"}
                    </div>
                    <span class="{badge_class}">{overall.upper()}</span>
                    <div style="margin-top:1rem; color:#718096; font-size:0.85rem;">
                        Confidence: {score_pct}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with s_col2:
                st.markdown('<div class="section-title">SENTIMENT BREAKDOWN</div>', unsafe_allow_html=True)
                # Render plotly gauge chart
                fig = render_sentiment_gauge(sentiment_data)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # Tone notes
            if sentiment_data.get("tone_notes"):
                st.markdown('<div class="section-title" style="margin-top:1rem;">TONE ANALYSIS</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="section-card">
                    <p style="color:#cbd5e0; line-height:1.7; font-size:0.92rem; margin:0;">
                        {sentiment_data["tone_notes"]}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Sentiment analysis not requested or unavailable.")

    # ── TAB 5: INSIGHTS (CHARTS) ──────────────
    with tabs[4]:
        st.markdown('<div class="section-title">VISUAL INSIGHTS</div>', unsafe_allow_html=True)
        ic1, ic2 = st.columns(2)

        with ic1:
            action_fig = render_action_item_chart(results)
            if action_fig:
                st.plotly_chart(action_fig, use_container_width=True, config={"displayModeBar": False})

        with ic2:
            topic_fig = render_topic_distribution(results)
            if topic_fig:
                st.plotly_chart(topic_fig, use_container_width=True, config={"displayModeBar": False})

        # Raw transcript preview
        with st.expander("🔍 View Original Transcript"):
            st.text_area(
                "Transcript",
                value=transcript,
                height=250,
                disabled=True,
                label_visibility="collapsed",
            )

    # ── EXPORT SECTION ────────────────────────
    st.markdown("---")
    st.markdown("#### 📤 Export Report")
    exp1, exp2 = st.columns(2)

    with exp1:
        # Build markdown export
        md_report = f"""# Meeting Intelligence Report

## Summary
{results.get('summary', 'N/A')}

## Action Items
{chr(10).join(f"- {item}" for item in results.get('action_items', []))}

## Key Decisions
{chr(10).join(f"- {d}" for d in results.get('decisions', []))}

## Sentiment
Overall: {results.get('sentiment', {}).get('overall', 'N/A')}

---
*Generated by MeetingIQ*
"""
        st.download_button(
            "⬇️ Download Markdown Report",
            data=md_report,
            file_name="meeting_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with exp2:
        import json
        st.download_button(
            "⬇️ Download JSON Data",
            data=json.dumps(results, indent=2),
            file_name="meeting_data.json",
            mime="application/json",
            use_container_width=True,
        )
