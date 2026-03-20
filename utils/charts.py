"""
charts.py
─────────
Plotly chart builders for the Meeting Intelligence System.
All charts use a dark theme consistent with the app's design.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Optional


# Shared dark theme config
DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#a0aec0"),
    margin=dict(l=10, r=10, t=30, b=10),
)


def render_sentiment_gauge(sentiment_data: dict) -> go.Figure:
    """
    Renders a half-circle gauge showing sentiment score (0-1).
    Color transitions: red → yellow → green.
    """
    score = float(sentiment_data.get("score", 0.5))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(score * 100, 1),
        number={"suffix": "%", "font": {"size": 28, "color": "#e2e8f0"}},
        title={"text": "Sentiment Score", "font": {"size": 13, "color": "#718096"}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "#4a5568",
                "tickfont": {"size": 11, "color": "#718096"},
            },
            "bar": {"color": _score_to_color(score), "thickness": 0.25},
            "bgcolor": "#1a2030",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 33], "color": "rgba(252, 129, 129, 0.15)"},
                {"range": [33, 66], "color": "rgba(246, 224, 94, 0.1)"},
                {"range": [66, 100], "color": "rgba(72, 187, 120, 0.12)"},
            ],
            "threshold": {
                "line": {"color": _score_to_color(score), "width": 3},
                "thickness": 0.75,
                "value": round(score * 100, 1),
            },
        },
    ))

    fig.update_layout(
        **DARK_LAYOUT,
        height=220,
    )
    return fig


def render_action_item_chart(results: dict) -> Optional[go.Figure]:
    """
    Bar chart showing action items grouped by owner (if available).
    Falls back to a simple count bar if no owner data.
    """
    items = results.get("action_items", [])
    if not items:
        return None

    # Count by owner
    owner_counts: dict = {}
    for item in items:
        if isinstance(item, dict):
            owner = item.get("owner", "Unassigned") or "Unassigned"
        else:
            owner = "Unassigned"
        owner_counts[owner] = owner_counts.get(owner, 0) + 1

    owners = list(owner_counts.keys())
    counts = list(owner_counts.values())
    colors = ["#4299e1", "#63b3ed", "#90cdf4", "#4a90d9", "#2b6cb0"]

    fig = go.Figure(go.Bar(
        x=owners,
        y=counts,
        marker_color=[colors[i % len(colors)] for i in range(len(owners))],
        text=counts,
        textposition="outside",
        textfont={"color": "#a0aec0", "size": 12},
    ))

    fig.update_layout(
        **DARK_LAYOUT,
        title={"text": "Action Items by Owner", "font": {"size": 13, "color": "#718096"}, "x": 0},
        height=260,
        xaxis={"gridcolor": "#2d3748", "tickfont": {"size": 11}},
        yaxis={"gridcolor": "#2d3748", "tickfont": {"size": 11}, "title": "Count"},
        bargap=0.35,
    )
    return fig


def render_topic_distribution(results: dict) -> Optional[go.Figure]:
    """
    Donut chart of key topics extracted from the meeting.
    """
    topics = results.get("key_topics", [])
    if not topics:
        return None

    # Equal weight for each topic (could be enhanced with relevance scores)
    values = [1] * len(topics)
    colors = [
        "#4299e1", "#48bb78", "#ed8936", "#9f7aea",
        "#f687b3", "#63b3ed", "#68d391", "#fbd38d",
    ]

    fig = go.Figure(go.Pie(
        labels=topics,
        values=values,
        hole=0.55,
        marker=dict(
            colors=colors[:len(topics)],
            line=dict(color="#0f1117", width=2),
        ),
        textfont={"size": 11, "color": "#e2e8f0"},
        hovertemplate="<b>%{label}</b><extra></extra>",
    ))

    fig.update_layout(
        **DARK_LAYOUT,
        title={"text": "Topic Distribution", "font": {"size": 13, "color": "#718096"}, "x": 0},
        height=260,
        legend=dict(
            font={"size": 10, "color": "#718096"},
            bgcolor="rgba(0,0,0,0)",
        ),
        annotations=[dict(
            text=f"{len(topics)}<br><span style='font-size:10px'>topics</span>",
            x=0.5, y=0.5,
            font_size=18,
            font_color="#e2e8f0",
            showarrow=False,
        )],
    )
    return fig


def _score_to_color(score: float) -> str:
    """Map a 0-1 score to a color: red → yellow → green."""
    if score >= 0.65:
        return "#48bb78"   # green
    elif score >= 0.4:
        return "#f6e05e"   # yellow
    else:
        return "#fc8181"   # red
