TREND_CLUSTERING_PROMPT = """Given this list of currently trending tracks
(title — channel), group them into mood clusters. Return strict JSON:
{{"clusters": {{"euphoric": ["title1", ...], "melancholic": [...]}}}}.

Trending tracks:
{track_list}"""
