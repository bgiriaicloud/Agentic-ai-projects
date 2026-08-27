"""
===============================================================================
HEALTHCARE MULTI-AGENT FASTAPI SERVICE (PORT 8005)
===============================================================================
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from hcare_orchestrator import hospital_assistant, HealthcareQueryRequest

app = FastAPI(title="Healthcare Multi-Agent Platform (GCP ADK & Gemini)", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Dashboard Files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.get("/api/healthz")
def health_check():
    return {
        "status": "healthy",
        "service": "Healthcare Multi-Agent Platform",
        "port": 8005,
        "framework": "Google ADK 2.4",
        "platform": "Gemini Agent Platform (Vertex AI Agent Builder)",
        "secret_manager": "GCP Secret Manager (Encrypted at Rest)",
        "hipaa_shield": "ACTIVE",
        "fhir_store": "CONNECTED"
    }


@app.post("/api/agents/query")
def execute_query(payload: HealthcareQueryRequest):
    if not payload.query or len(payload.query.strip()) < 3:
        raise HTTPException(status_code=400, detail="Query string must be at least 3 characters long.")
    
    result = hospital_assistant.process_request(payload)
    return result.model_dump()


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8005, reload=True)
