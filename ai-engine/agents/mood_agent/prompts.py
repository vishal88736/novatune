# Mood Agent is mostly deterministic (GoEmotions classifier), but uses the
# fast LLM tier to map a mood-wheel tap label (no free text) onto a
# plausible emotion-score distribution, so downstream agents always receive
# a consistent 27-dim vector regardless of input modality.
TAP_TO_EMOTION_PROMPT = """Given the single mood label "{label}", output your
best-guess distribution across these GoEmotions classes as strict JSON
mapping class name to a 0-1 score (they don't need to sum to 1): admiration,
amusement, anger, annoyance, approval, caring, confusion, curiosity, desire,
disappointment, disapproval, disgust, embarrassment, excitement, fear,
gratitude, grief, joy, love, nervousness, optimism, pride, realization,
relief, remorse, sadness, surprise, neutral."""
