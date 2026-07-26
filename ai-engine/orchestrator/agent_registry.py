"""Registers all 11 agents behind a uniform lookup so the planner and the
FastAPI router never need to know each agent's concrete import path."""

from agents.analytics_agent.agent import AnalyticsAgent
from agents.base import BaseAgent
from agents.conversation_agent.agent import ConversationAgent
from agents.discovery_agent.agent import DiscoveryAgent
from agents.explainability_agent.agent import ExplainabilityAgent
from agents.memory_agent.agent import MemoryAgent
from agents.mood_agent.agent import MoodAgent
from agents.playlist_upload_analysis_agent.agent import PlaylistUploadAnalysisAgent
from agents.recommendation_agent.agent import RecommendationAgent
from agents.sequencing_agent.agent import SequencingAgent
from agents.taste_profiling_agent.agent import TasteProfilingAgent
from agents.trend_analysis_agent.agent import TrendAnalysisAgent

AGENT_REGISTRY: dict[str, BaseAgent] = {
    "conversation_agent": ConversationAgent(),
    "mood_agent": MoodAgent(),
    "taste_profiling_agent": TasteProfilingAgent(),
    "playlist_upload_analysis_agent": PlaylistUploadAnalysisAgent(),
    "recommendation_agent": RecommendationAgent(),
    "sequencing_agent": SequencingAgent(),
    "memory_agent": MemoryAgent(),
    "discovery_agent": DiscoveryAgent(),
    "trend_analysis_agent": TrendAnalysisAgent(),
    "explainability_agent": ExplainabilityAgent(),
    "analytics_agent": AnalyticsAgent(),
}


def get_agent(name: str) -> BaseAgent:
    if name not in AGENT_REGISTRY:
        raise KeyError(f"Unknown agent: {name}")
    return AGENT_REGISTRY[name]
