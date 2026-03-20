"""
parser.py
─────────
Utility functions for parsing and cleaning transcript data
before and after LLM analysis.
"""

import re
from typing import Optional


def extract_sections(text: str) -> dict:
    """
    Pre-processes a raw transcript to extract metadata before sending to LLM.
    Identifies speaker names, estimates duration, and cleans noise.

    Args:
        text: Raw transcript string.

    Returns:
        dict with cleaned_text, speakers, line_count, word_count.
    """
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    word_count = len(text.split())
    line_count = len(lines)

    # Detect speaker patterns: "Name:" or "[Name]:" or "Name (role):"
    speaker_pattern = re.compile(r"^([A-Za-z][A-Za-z\s\-\.]{0,30}?)(?:\s*[\[\(][^\]\)]*[\]\)])?\s*:")
    speakers = []
    for line in lines:
        match = speaker_pattern.match(line)
        if match:
            name = match.group(1).strip()
            if name and name not in speakers:
                speakers.append(name)

    # Clean the transcript: remove timestamps like [00:04:12], [HH:MM:SS]
    clean = re.sub(r"\[\d{1,2}:\d{2}(?::\d{2})?\]", "", text)
    clean = re.sub(r"\(\d{1,2}:\d{2}(?::\d{2})?\)", "", clean)
    # Remove excessive whitespace
    clean = re.sub(r"\n{3,}", "\n\n", clean).strip()

    return {
        "cleaned_text": clean,
        "speakers": speakers,
        "line_count": line_count,
        "word_count": word_count,
        "estimated_duration_min": _estimate_duration(word_count),
    }


def _estimate_duration(word_count: int) -> Optional[float]:
    """
    Rough estimate of meeting duration based on average speaking pace.
    Average conversational speech: ~130 words/minute.
    """
    if word_count <= 0:
        return None
    return round(word_count / 130, 1)


def clean_action_item(item) -> str:
    """Normalize an action item to a plain string for display."""
    if isinstance(item, dict):
        parts = [item.get("task", "")]
        if item.get("owner"):
            parts.append(f"(Owner: {item['owner']})")
        if item.get("deadline"):
            parts.append(f"(Due: {item['deadline']})")
        return " ".join(p for p in parts if p)
    return str(item)
