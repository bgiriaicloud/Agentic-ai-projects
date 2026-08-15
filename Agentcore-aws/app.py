"""
Amazon AgentCore - Web API Server
---------------------------------
FastAPI server serving the AgentCore Engine API endpoints and static interactive web UI.
"""

import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from agentcore_sdk import AgentCoreRuntime
from agent import FinOpsAgentCoreAgent

load_dotenv()

execution_mode = os.getenv("EXECUTION_MODE", "mock")
runtime = AgentCoreRuntime(execution_mode=execution_mode)
agent = FinOpsAgentCoreAgent(runtime)

app = FastAPI(
    title="Amazon AgentCore Web API",
    description="Agentic framework with Serverless Runtime, Memory, MCP Gateway, and Observability.",
    version="1.0.0"
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


class CreateSessionRequest(BaseModel):
    metadata: Optional[Dict[str, Any]] = None


class RunAgentRequest(BaseModel):
    session_id: Optional[str] = None
    prompt: str = Field(..., example="Calculate monthly cost for 4 EC2 t3.large instances and scan S3 log bucket")


@app.get("/")
async def get_index():
    """Serve main web interface."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"status": "AgentCore API running."})


@app.post("/api/sessions")
async def create_session(req: Optional[CreateSessionRequest] = None):
    """Create a new isolated AgentCore execution session."""
    meta = req.metadata if req else {}
    session = runtime.create_session(metadata=meta)
    return session.model_dump()


@app.post("/api/agent/run")
async def run_agent_turn(req: RunAgentRequest):
    """Run turn of AgentCore agent reasoning loop."""
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    session_id = req.session_id
    if not session_id or not runtime.get_session(session_id):
        session = runtime.create_session()
        session_id = session.session_id

    try:
        res = agent.run(session_id=session_id, prompt=req.prompt)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agent/memory/{session_id}")
async def get_session_memory(session_id: str):
    """Inspect short-term conversation history and long-term facts for a session."""
    session = runtime.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")

    history = runtime.memory.get_history(session_id)
    facts = runtime.memory.get_long_term_facts(session_id)

    return {
        "session_id": session_id,
        "history": [m.model_dump() for m in history],
        "long_term_facts": facts
    }


@app.get("/api/agent/tools")
async def list_gateway_tools():
    """List all registered AgentCore Gateway tools."""
    return {"tools": runtime.gateway.list_tools()}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Amazon AgentCore Platform Demo",
        "execution_mode": runtime.execution_mode,
        "active_sessions": len(runtime._active_sessions)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
