"""
Env-driven provider selection. Currently only Groq is wired, but agents
resolve their LLM through this factory (never importing GroqProvider
directly) so a future provider swap is a one-line change here.
"""

from providers.llm.base_provider import LLMProvider
from providers.llm.groq_provider import groq_provider


def get_llm_provider() -> LLMProvider:
    return groq_provider
