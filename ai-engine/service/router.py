from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from agents.conversation_agent.agent import ConversationAgent
from orchestrator.agent_registry import get_agent
from orchestrator.streaming import format_stream
from service.deps import build_context

router = APIRouter()


@router.post("/agents/{agent_name}/invoke")
async def invoke_agent(agent_name: str, payload: dict) -> dict:
    try:
        agent = get_agent(agent_name)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    user_id = payload.pop("user_id")
    session_id = payload.pop("session_id", None)
    ctx = await build_context(user_id, session_id, payload)

    result = await agent.run(ctx)
    return result.data


@router.post("/agents/conversation_agent/stream")
async def stream_conversation(payload: dict) -> StreamingResponse:
    """
    Dedicated streaming path for the Conversation Agent — the only agent
    whose output is token-streamed directly to the end user.
    """
    agent = ConversationAgent()
    ctx = await build_context(payload["user_id"], payload.get("session_id"), payload)
    return StreamingResponse(format_stream(agent.stream_reply(ctx)), media_type="text/event-stream")


@router.post("/pipeline/recommendation/run")
async def run_recommendation_pipeline(payload: dict) -> dict:
    agent = get_agent("recommendation_agent")
    ctx = await build_context(payload["user_id"], None, payload)
    result = await agent.run(ctx)
    return result.data


@router.post("/pipeline/embedding/run")
async def run_embedding_pipeline(payload: dict) -> dict:
    from pipelines.embedding_pipeline import embed_tracks_batch

    embed_tracks_batch(payload.get("tracks", []))
    return {"status": "embedded", "count": len(payload.get("tracks", []))}
