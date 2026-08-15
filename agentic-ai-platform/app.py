"""
Web API Server & Web UI - Enterprise Agentic AI Platform
---------------------------------------------------------
Serves the Agentic Platform REST API endpoints and static interactive web testing dashboard on port 8003.
"""

import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from agents.supervisor_agent import SupervisorAgent
from mcp_servers.mcp_gcp_server import mcp_server

load_dotenv()

execution_mode = os.getenv("EXECUTION_MODE", "mock")
supervisor = SupervisorAgent()

app = FastAPI(
    title="Enterprise Agentic AI Platform API",
    description="Multi-agent orchestration platform with ADK, FastMCP, and A2A subagents.",
    version="1.0.0"
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


class RunOrchestrationRequest(BaseModel):
    prompt: str = Field(..., example="Run full infrastructure audit and calculate BigQuery billing spend")
    session_id: Optional[str] = None


@app.get("/")
async def get_index():
    """Serve main web interface."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"status": "Agentic Platform API running."})


@app.post("/api/orchestrate")
async def run_orchestration(req: RunOrchestrationRequest):
    """Run Supervisor Master Agent A2A orchestration."""
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    try:
        res = supervisor.orchestrate(req.prompt, session_id=req.session_id)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/mcp/tools")
async def list_mcp_tools():
    """List tools exposed by FastMCP server."""
    return {"tools": mcp_server.list_tools()}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Enterprise Agentic AI Platform",
        "supervisor_agent": supervisor.name,
        "execution_mode": execution_mode,
        "mcp_server": mcp_server.name
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
