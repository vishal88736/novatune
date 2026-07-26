EXPLANATION_PROMPT = """Explain in 2-3 warm, specific sentences why this
track was recommended to this listener right now. Do not sound like a
recommendation-engine log — sound like a friend explaining their reasoning.

Track: {track_title} by {artist}
Listener's current mood: {mood_label}
Signals and their weights: {signals}"""
