"""
audio_processor.py
──────────────────
Handles audio transcription using OpenAI's Whisper model.
Supports .mp3, .wav, .m4a, and more.
"""

from openai import OpenAI
import os

def transcribe_audio(file_path: str, api_key: str) -> str:
    """
    Transcribes an audio file using OpenAI Whisper API.
    
    Args:
        file_path: Path to the audio file on disk.
        api_key:   OpenAI API key.
        
    Returns:
        The transcribed text.
    """
    client = OpenAI(api_key=api_key)
    
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="text"
        )
    return transcript

def get_mock_transcription() -> str:
    """
    Returns a high-quality mock transcript for Demo Mode.
    """
    return (
        "Sarah: Good morning everyone. Let me start the Q3 product strategy review. "
        "John, what's the status on Feature X? "
        "John: We're on track for a mid-August release. The backend is 90% complete. "
        "Lisa: That's great. I have the initial design mockups ready for review by Friday. "
        "Sarah: Excellent. Let's make a decision — we'll ship Feature X as the main priority for Q3. "
        "John: Agreed. However, I'm concerned about the technical debt we're carrying. "
        "Sarah: Good point. Let's move the tech debt tasks to a dedicated sprint in Q4 to keep our current momentum. "
        "Lisa: Sounds like a plan. I'll sync with the frontend team to ensure the designs are aligned with the new estimates. "
        "Sarah: Perfect. John, send me the final estimates by Wednesday. Meeting adjourned."
    )
