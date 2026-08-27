"""
Google Cloud Enterprise Agent Platform - Web API Server
--------------------------------------------------------
FastAPI server serving the GCP Agent Platform REST API endpoints and static interactive web UI.
"""

import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from gcp_agent_platform_sdk import AgentPlatformRuntime
from agent import GCPEnterpriseAgent

load_dotenv()

execution_mode = os.getenv("EXECUTION_MODE", "mock")
project_id = os.getenv("GCP_PROJECT_ID", "gcp-10-project")

runtime = AgentPlatformRuntime(execution_mode=execution_mode, project_id=project_id)
agent = GCPEnterpriseAgent(runtime)

app = FastAPI(
    title="Google Cloud Enterprise Agent Platform API",
    description="Build, Scale, Govern, and Optimize Enterprise AI Agents.",
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
    prompt: str = Field(..., example="Run Vertex AI search for GKE and query BigQuery costs")


@app.get("/")
async def get_index():
    """Serve main web interface."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"status": "GCP Agent Platform running."})


@app.post("/api/sessions")
async def create_session(req: Optional[CreateSessionRequest] = None):
    """Create a new isolated GCP Agent session container."""
    meta = req.metadata if req else {}
    session = runtime.create_session(metadata=meta)
    return session.model_dump()


@app.post("/api/agent/run")
async def run_agent_turn(req: RunAgentRequest):
    """Run turn of GCP Enterprise Agent across the 4 Pillars."""
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


@app.get("/api/agent/extensions")
async def list_vertex_extensions():
    """List all registered Vertex AI Extensions."""
    return {"extensions": runtime.extensions.list_extensions()}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Google Cloud Enterprise Agent Platform",
        "project_id": runtime.project_id,
        "execution_mode": runtime.execution_mode,
        "active_sessions": len(runtime._sessions)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True)
