RERANK_PROMPT = """You are ranking music track candidates for a listener
whose current mood is "{mood_label}" (valence {valence}, arousal {arousal})
and whose top genres are {top_genres}.

Score each candidate from 0-1 on: mood_fit, novelty, and overall priority.
Return strict JSON: {{"rankings": [{{"id": "...", "mood_fit": 0.0,
"novelty": 0.0, "priority": 0.0}}, ...]}}, ordered by priority descending.

Candidates:
{candidates}"""
