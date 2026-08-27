"""
Azure AI Search - Agentic Retrieval Web API Server
--------------------------------------------------
FastAPI server serving the Agentic Retrieval Engine API endpoints and static interactive UI.
"""

import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from agentic_retrieval_engine import (
    AgenticRetrievalEngine,
    ReasoningEffort,
    MOCK_KNOWLEDGE_SOURCES
)

# Load environment variables
load_dotenv()

execution_mode = os.getenv("EXECUTION_MODE", "mock")
engine = AgenticRetrievalEngine(execution_mode=execution_mode)

app = FastAPI(
    title="Azure AI Search Agentic Retrieval API",
    description="Multi-query pipeline for complex questions, RAG, and agentic workflows.",
    version="1.0.0"
)

# Mount static folder for web UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


class RetrievalRequest(BaseModel):
    query: str = Field(..., example="Find me a hotel near the beach, with airport shuttle, and near vegetarian restaurants")
    chat_history: Optional[List[Dict[str, str]]] = Field(default=None)
    reasoning_effort: ReasoningEffort = Field(default=ReasoningEffort.LOW)


@app.get("/")
async def get_index():
    """Serve main web interface."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"status": "API active. Upload static/index.html to view UI."})


@app.post("/api/retrieval")
async def execute_agentic_retrieval(req: RetrievalRequest):
    """
    Execute Agentic Retrieval pipeline.
    Decomposes queries, searches parallel knowledge sources, applies L2 semantic reranking, and synthesizes answer.
    """
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        result = engine.execute_retrieval(
            query=req.query,
            chat_history=req.chat_history,
            reasoning_effort=req.reasoning_effort
        )
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/knowledge-sources")
async def list_knowledge_sources():
    """List all registered Knowledge Sources & search index configurations."""
    sources = []
    for k, v in MOCK_KNOWLEDGE_SOURCES.items():
        sources.append({
            "id": v["id"],
            "name": v["name"],
            "type": v["type"].value,
            "search_type": v["search_type"].value,
            "doc_count": len(v["documents"])
        })
    return {"knowledge_sources": sources}


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Azure AI Search Agentic Retrieval Demo",
        "execution_mode": engine.execution_mode,
        "azure_search_configured": bool(engine.azure_search_endpoint and engine.azure_search_key),
        "azure_openai_configured": bool(engine.azure_openai_endpoint and engine.azure_openai_key)
    }


@app.post("/api/simulate-azure-payload")
async def simulate_azure_rest_payload(req: RetrievalRequest):
    """
    Generates exact Azure AI Search REST API payload (2026-05-01-preview) for knowledge retrieval action.
    """
    payload = {
        "api_version": "2026-05-01-preview",
        "method": "POST",
        "url": f"https://{engine.azure_search_endpoint or 'YOUR_SEARCH_SERVICE'}.search.windows.net/knowledgebases/kb-agentic/retrieve?api-version=2026-05-01-preview",
        "headers": {
            "Content-Type": "application/json",
            "api-key": "[AZURE_SEARCH_ADMIN_KEY]"
        },
        "body": {
            "query": req.query,
            "reasoningEffort": req.reasoning_effort.value,
            "conversationHistory": req.chat_history or [],
            "options": {
                "includeActivityLog": True,
                "includeCitations": True,
                "semanticReranking": "enabled",
                "top": 5
            }
        }
    }
    return payload


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
