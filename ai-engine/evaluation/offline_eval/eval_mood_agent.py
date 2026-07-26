"""
Regression check for the Mood Agent's text→emotion mapping against a small
labeled golden set. Run in CI on every prompt/model change (see
infra/ci/ai-engine-ci.yml) to catch silent quality regressions.
"""

import json
from pathlib import Path

from providers.emotion.goemotions_provider import goemotions_provider

GOLDEN_SET_PATH = Path(__file__).parent.parent / "golden_sets" / "mood_agent_cases.json"


def run_eval() -> dict:
    cases = json.loads(GOLDEN_SET_PATH.read_text())
    correct = 0
    for case in cases:
        scores = goemotions_provider.classify(case["text"])
        predicted = goemotions_provider.dominant_label(scores)
        if predicted == case["expected_label"]:
            correct += 1
    accuracy = correct / len(cases) if cases else 0.0
    return {"accuracy": accuracy, "total": len(cases), "correct": correct}


if __name__ == "__main__":
    print(run_eval())
