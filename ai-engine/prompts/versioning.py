"""
Prompt version registry. Each agent's prompt module can register multiple
versions here; the active version per environment is resolved centrally so
a bad prompt change can be rolled back without a code deploy.
"""

import os

ACTIVE_VERSIONS: dict[str, str] = {
    "conversation_agent": "v1",
    "mood_agent": "v1",
    "recommendation_agent": "v1",
    "explainability_agent": "v1",
}


def get_active_version(agent_name: str) -> str:
    override = os.environ.get(f"PROMPT_VERSION_{agent_name.upper()}")
    return override or ACTIVE_VERSIONS.get(agent_name, "v1")
