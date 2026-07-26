# Taste Profiling is primarily a numeric aggregation over listening history
# embeddings (see pipelines/embedding_pipeline.py); no LLM prompt is needed
# for the core computation. Reserved for future natural-language taste
# summaries (e.g. "you gravitate toward melancholic indie folk at night").
TASTE_SUMMARY_PROMPT = """Summarize this user's music taste in one warm,
specific sentence based on their top genres and artists: {profile_json}"""
