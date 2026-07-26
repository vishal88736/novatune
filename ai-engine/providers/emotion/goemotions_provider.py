"""
GoEmotions-based emotion classifier (27 fine-grained emotion classes +
neutral), served locally via a HuggingFace `text-classification` pipeline.
Output is normalized into a valence/arousal pair for downstream agents that
just need a coarse mood direction, alongside the raw 27-dim score vector for
agents (like Explainability) that want the nuance.
"""

from functools import lru_cache

from transformers import pipeline

from service.config import settings

# Approximate valence/arousal coordinates per GoEmotions label, used to
# project the 27-class distribution into a 2D mood space for the UI's mood
# wheel / timeline. Values are illustrative placements on a circumplex model.
VALENCE_AROUSAL_MAP: dict[str, tuple[float, float]] = {
    "admiration": (0.6, 0.3), "amusement": (0.7, 0.5), "anger": (-0.6, 0.7),
    "annoyance": (-0.4, 0.5), "approval": (0.5, 0.1), "caring": (0.5, 0.2),
    "confusion": (-0.2, 0.3), "curiosity": (0.3, 0.4), "desire": (0.4, 0.6),
    "disappointment": (-0.5, -0.1), "disapproval": (-0.4, 0.2), "disgust": (-0.6, 0.4),
    "embarrassment": (-0.3, 0.3), "excitement": (0.7, 0.8), "fear": (-0.6, 0.7),
    "gratitude": (0.7, 0.2), "grief": (-0.8, -0.3), "joy": (0.8, 0.5),
    "love": (0.8, 0.4), "nervousness": (-0.3, 0.6), "optimism": (0.6, 0.3),
    "pride": (0.6, 0.4), "realization": (0.1, 0.2), "relief": (0.5, -0.3),
    "remorse": (-0.6, -0.1), "sadness": (-0.7, -0.4), "surprise": (0.2, 0.7),
    "neutral": (0.0, 0.0),
}


@lru_cache(maxsize=1)
def _classifier():
    return pipeline(
        "text-classification",
        model=settings.goemotions_model_name,
        top_k=None,
        truncation=True,
    )


class GoEmotionsProvider:
    def classify(self, text: str) -> dict[str, float]:
        raw = _classifier()(text)[0]
        return {item["label"]: round(float(item["score"]), 4) for item in raw}

    def to_valence_arousal(self, scores: dict[str, float]) -> tuple[float, float]:
        total_weight = sum(scores.values()) or 1.0
        valence = sum(
            scores[label] * VALENCE_AROUSAL_MAP.get(label, (0.0, 0.0))[0] for label in scores
        ) / total_weight
        arousal = sum(
            scores[label] * VALENCE_AROUSAL_MAP.get(label, (0.0, 0.0))[1] for label in scores
        ) / total_weight
        return round(valence, 3), round(arousal, 3)

    def dominant_label(self, scores: dict[str, float]) -> str:
        return max(scores, key=lambda k: scores[k])


goemotions_provider = GoEmotionsProvider()
