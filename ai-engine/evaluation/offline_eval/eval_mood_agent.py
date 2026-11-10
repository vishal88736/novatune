"""
Regression check for the Mood Agent's text→emotion mapping against a small
labeled golden set. Run in CI on every prompt/model change (see
.github/workflows/ai-engine-ci.yml) to catch silent quality regressions.

Each case names an `expected_label`. GoEmotions often ranks two closely
related emotions within a hair of each other ("joy" vs "excitement",
"anger" vs "annoyance"), and which one wins is not a defect — so a case
may also list `acceptable_labels`, any of which count as a pass. Cases
without alternatives are strict.
"""

import json
import sys
from pathlib import Path
from typing import Any

from providers.emotion.goemotions_provider import goemotions_provider

GOLDEN_SET_PATH = Path(__file__).parent.parent / "golden_sets" / "mood_agent_cases.json"

# Accuracy below this fails CI. Set just under the current model's score so
# that a genuine regression trips it while ordinary model drift does not.
MIN_ACCURACY = 0.85


def evaluate_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    correct = 0
    failures: list[dict[str, Any]] = []

    for case in cases:
        scores = goemotions_provider.classify(case["text"])
        predicted = goemotions_provider.dominant_label(scores)
        expected = case["expected_label"]
        accepted = {expected, *case.get("acceptable_labels", [])}

        if predicted in accepted:
            correct += 1
        else:
            failures.append(
                {
                    "text": case["text"],
                    "expected": expected,
                    "predicted": predicted,
                    "top_scores": dict(
                        sorted(scores.items(), key=lambda kv: -kv[1])[:3]
                    ),
                }
            )

    total = len(cases)
    return {
        "accuracy": correct / total if total else 0.0,
        "total": total,
        "correct": correct,
        "failures": failures,
    }


def run_eval() -> dict[str, Any]:
    cases = json.loads(GOLDEN_SET_PATH.read_text())
    return evaluate_cases(cases)


def main() -> int:
    result = run_eval()
    print(
        f"accuracy={result['accuracy']:.2%} "
        f"({result['correct']}/{result['total']}) threshold={MIN_ACCURACY:.0%}"
    )
    for failure in result["failures"]:
        print(
            f"  MISS {failure['text']!r}\n"
            f"       expected={failure['expected']} predicted={failure['predicted']} "
            f"top={failure['top_scores']}"
        )

    if result["accuracy"] < MIN_ACCURACY:
        print(f"FAIL: accuracy below {MIN_ACCURACY:.0%}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
