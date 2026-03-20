"""
llm_client.py
─────────────
Handles all OpenAI API interactions for the Meeting Intelligence System.
Uses a structured multi-prompt approach to extract distinct signals from transcripts.
"""

import json
import re
import requests
from openai import OpenAI


# ─────────────────────────────────────────────
# SYSTEM PROMPT — sets LLM persona & rules
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are MeetingIQ, an elite AI meeting analyst trusted by Fortune 500 companies.
Your role is to extract precise, actionable intelligence from meeting transcripts.

Rules:
- Be concise but comprehensive
- Focus on facts, not speculation
- Return structured JSON exactly as requested
- Never invent information not present in the transcript
- For sentiment, base your score on the overall conversational tone, not just keywords
"""


def analyze_transcript(
    transcript: str,
    api_key: str,
    model: str = "gpt-4o",
    do_summary: bool = True,
    do_actions: bool = True,
    do_decisions: bool = True,
    do_sentiment: bool = True,
) -> dict:
    """
    Main entry point. Sends the transcript to OpenAI with a structured
    prompt, then parses the JSON response into a clean result dict.

    Args:
        transcript:     Raw meeting transcript text.
        api_key:        OpenAI API key.
        model:          Model identifier (e.g., "gpt-4o").
        do_summary:     Whether to generate a meeting summary.
        do_actions:     Whether to extract action items.
        do_decisions:   Whether to extract key decisions.
        do_sentiment:   Whether to perform sentiment analysis.

    Returns:
        dict with keys: summary, action_items, decisions, sentiment, key_topics
    """
    client = OpenAI(api_key=api_key)

    # Build a dynamic user prompt based on selected options
    sections_requested = _build_sections_prompt(
        do_summary, do_actions, do_decisions, do_sentiment
    )

    user_prompt = f"""Analyze this meeting transcript and return a JSON object with the following structure:

{sections_requested}

MEETING TRANSCRIPT:
\"\"\"
{transcript}
\"\"\"

Return ONLY valid JSON. No explanation, no markdown fences — just the raw JSON object."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,     # Low temp for factual extraction
        max_tokens=2048,
        response_format={"type": "json_object"},  # Force JSON mode (GPT-4o+)
    )

    raw = response.choices[0].message.content
    return _safe_parse(raw)


def _build_sections_prompt(
    do_summary: bool,
    do_actions: bool,
    do_decisions: bool,
    do_sentiment: bool,
) -> str:
    """
    Dynamically constructs the JSON schema description based on
    which analysis modules are enabled by the user.
    """
    schema_parts = []

    if do_summary:
        schema_parts.append(
            '"summary": "A 3-5 sentence executive summary of the meeting"'
        )
        schema_parts.append(
            '"key_topics": ["Array of 3-6 main topics discussed as short phrases"]'
        )

    if do_actions:
        schema_parts.append(
            '"action_items": [{"task": "Description of task", "owner": "Person responsible or empty string", "deadline": "Deadline if mentioned or empty string"}]'
        )

    if do_decisions:
        schema_parts.append(
            '"decisions": ["Array of clear decisions made during the meeting"]'
        )

    if do_sentiment:
        schema_parts.append(
            '"sentiment": {"overall": "positive|negative|neutral", "score": 0.0_to_1.0_float, "tone_notes": "2-3 sentence description of the meeting tone and emotional dynamics"}'
        )

    if not schema_parts:
        return '{"message": "No analysis sections were selected."}'

    schema_str = "{\n  " + ",\n  ".join(schema_parts) + "\n}"
    return schema_str


def _safe_parse(raw: str) -> dict:
    """
    Safely parse JSON from LLM output.
    Handles edge cases where the model may include extra text or backticks.
    """
    # Strip any accidental markdown fences
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return a structured error response
        return {
            "summary": "Analysis failed — could not parse LLM response.",
            "action_items": [],
            "decisions": [],
            "sentiment": {
                "overall": "neutral",
                "score": 0.5,
                "tone_notes": "Could not analyze sentiment.",
            },
            "key_topics": [],
            "_error": raw[:200],
        }


def get_mock_analysis() -> dict:
    """
    Returns high-quality mock analytical data for demonstration purposes.
    Allows testing the UI and features without an OpenAI API key.
    """
    return {
        "summary": "The Q3 Product Strategy meeting focused on finalizing the roadmap for the upcoming quarter. Key priorities include shipping Feature X by mid-August and initiating the design phase for Project Y. The team discussed resource allocation and decided to move technical debt tasks to a separate sprint to ensure timeline adherence.",
        "key_topics": ["Q3 Roadmap", "Feature X Timeline", "Project Y Design", "Resource Allocation"],
        "action_items": [
            {"task": "Finalize Feature X engineering estimates", "owner": "John", "deadline": "Wednesday"},
            {"task": "Prepare Project Y design mockups", "owner": "Lisa", "deadline": "Friday"},
            {"task": "Schedule follow-up meeting with stakeholders", "owner": "Sarah", "deadline": "Next Monday"}
        ],
        "decisions": [
            "Feature X is prioritized for Q3 release.",
            "Project Y design phase begins immediately.",
            "Technical debt sprint deferred to Q4."
        ],
        "sentiment": {
            "overall": "positive",
            "score": 0.85,
            "tone_notes": "The meeting was highly collaborative and productive. Team members were aligned on priorities, though some concerns were raised regarding timeline buffers which were successfully addressed."
        }
    }


def analyze_transcript_ollama(
    transcript: str,
    model: str = "llama3",
    do_summary: bool = True,
    do_actions: bool = True,
    do_decisions: bool = True,
    do_sentiment: bool = True,
) -> dict:
    """
    Analyzes the transcript using a local Ollama instance.
    No API key required.
    """
    url = "http://localhost:11434/api/chat"
    
    sections_requested = _build_sections_prompt(
        do_summary, do_actions, do_decisions, do_sentiment
    )
    
    user_prompt = f"""Analyze this meeting transcript and return a JSON object with the following structure:

{sections_requested}

MEETING TRANSCRIPT:
\"\"\"
{transcript}
\"\"\"

Return ONLY valid JSON. No explanation, no markdown fences — just the raw JSON object."""

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "format": "json",
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        raw = response.json()["message"]["content"]
        return _safe_parse(raw)
    except Exception as e:
        return {
            "summary": f"Ollama Error: {str(e)}. Ensure Ollama is running at localhost:11434.",
            "action_items": [],
            "decisions": [],
            "sentiment": {"overall": "neutral", "score": 0.5, "tone_notes": ""},
            "key_topics": [],
            "_error": str(e)
        }
