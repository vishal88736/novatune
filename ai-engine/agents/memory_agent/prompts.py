MILESTONE_DETECTION_PROMPT = """Given this week's mood log summary, identify
whether a significant emotional milestone occurred (a clear turning point,
sustained low, or notable high). If so, return strict JSON:
{{"is_milestone": true, "label": "...", "detail": "..."}}. If not, return
{{"is_milestone": false}}.

Mood log summary: {mood_summary}"""

JOURNEY_SUMMARY_PROMPT = """Write a brief, compassionate one-paragraph
summary of this listener's emotional journey over the past period, based on
these mood log entries. Avoid clinical language; write like a thoughtful
friend reflecting back what they've noticed. Entries: {entries}"""
