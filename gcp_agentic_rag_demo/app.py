"""
===============================================================================
GCP AGENTIC RAG FASTAPI WEB SERVER (PORT 8004)
===============================================================================
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional

from gcp_rag_engine import GCPAgenticRAGEngine

app = FastAPI(title="GCP Agentic RAG Demo Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = GCPAgenticRAGEngine()

# Serve Static Web Dashboard Files
app.mount("/static", StaticFiles(directory="static"), name="static")


class QueryPayload(BaseModel):
    query: str


class IngestPayload(BaseModel):
    file_name: str
    source: Optional[str] = "Cloud Storage (GCS)"
    content: str


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.get("/api/healthz")
def health_check():
    return {"status": "healthy", "service": "GCP Agentic RAG Demo Platform", "port": 8004}


@app.post("/api/rag/query")
def execute_query(payload: QueryPayload):
    if not payload.query or len(payload.query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Query string must be at least 3 characters long.")
    
    result = engine.execute_agentic_rag(payload.query)
    return result.dict()


@app.post("/api/rag/ingest")
def ingest_event(payload: IngestPayload):
    if not payload.file_name or not payload.content:
        raise HTTPException(status_code=400, detail="file_name and content are required.")
    
    result = engine.process_pubsub_event(payload.dict())
    return result


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8004, reload=True)
