GENRE_MOOD_TAGGING_PROMPT = """Given this list of tracks (title — artist),
output strict JSON with two keys: "genre_breakdown" and "mood_breakdown",
each mapping a short label to a 0-1 proportion (should each sum to ~1).
Base this on your general knowledge of these tracks/artists.

Tracks:
{track_list}"""

TASTE_DELTA_PROMPT = """In one encouraging sentence, describe what this
uploaded playlist reveals or reinforces about the listener's taste, given
their existing genre affinities: {existing_profile}
New playlist genre breakdown: {new_breakdown}"""
