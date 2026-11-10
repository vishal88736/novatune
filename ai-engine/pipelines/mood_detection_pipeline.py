"""Wraps the GoEmotions provider into the normalized mood-vector output
consumed everywhere else in the system."""

from typing import Any

from providers.emotion.goemotions_provider import goemotions_provider


def detect_mood_from_text(text: str) -> dict[str, Any]:
    scores = goemotions_provider.classify(text)
    valence, arousal = goemotions_provider.to_valence_arousal(scores)
    return {
        "label": goemotions_provider.dominant_label(scores).capitalize(),
        "valence": valence,
        "arousal": arousal,
        "emotion_scores": scores,
    }
