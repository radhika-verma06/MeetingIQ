"""Small smoke test for MeetingIQ's demo data and charts."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.llm_client import get_mock_analysis
from utils.audio_processor import get_mock_transcription
from utils.charts import render_sentiment_gauge, render_action_item_chart, render_topic_distribution


def test_demo_pipeline():
    results = get_mock_analysis()
    transcript = get_mock_transcription()
    assert results["summary"]
    assert len(transcript.split()) > 20
    assert render_sentiment_gauge(results) is not None
    assert render_action_item_chart(results) is not None
    assert render_topic_distribution(results) is not None


if __name__ == "__main__":
    test_demo_pipeline()
    print("MeetingIQ demo smoke test passed")
