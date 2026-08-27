import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google.antigravity import Agent, LocalAgentConfig, types
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

app = FastAPI(title="Agentic AI Testing Dashboard")

# Request Model
class ChatRequest(BaseModel):
    message: str

# Helper to run the agent and capture thoughts and text response
async def run_agent_workflow(config: LocalAgentConfig, prompt: str):
    try:
        async with Agent(config=config) as agent:
            response = await agent.chat(prompt)
            
            # Capture thoughts
            thoughts = []
            async for thought in response.thoughts:
                thoughts.append(thought)
            
            # Capture final text response
            response_text = []
            async for chunk in response:
                response_text.append(chunk)
                
            return {
                "status": "success",
                "thoughts": "".join(thoughts),
                "response": "".join(response_text)
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/api/chat/adk")
async def chat_adk(payload: ChatRequest):
    # Configure the basic ADK agent (Cloud Solutions Architect)
    def calculate_vm_cost(instance_count: int, hours: int, cost_per_hour: float = 0.10) -> str:
        """Calculates the estimated compute engine instance hosting cost."""
        total_cost = instance_count * hours * cost_per_hour
        return f"Estimated cost for {instance_count} GCE VMs running {hours} hours is ${total_cost:.2f}."

    config = LocalAgentConfig(
        system_instructions=(
            "You are a Cloud Solutions Architect specializing in GCP. "
            "You help users size GCE compute VM resource configurations. Use calculate_vm_cost tool when appropriate."
        ),
        tools=[calculate_vm_cost],
    )
    result = await run_agent_workflow(config, payload.message)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@app.post("/api/chat/mcp")
async def chat_mcp(payload: ChatRequest):
    # Configure agent with local MCP server running via Stdio
    mcp_server_script = os.path.join(os.path.dirname(__file__), "mcp_server.py")
    if not os.path.exists(mcp_server_script):
        raise HTTPException(status_code=500, detail="mcp_server.py script not found.")
        
    mcp_servers = [
        types.McpStdioServer(
            command="python3",
            args=[mcp_server_script],
        )
    ]
    config = LocalAgentConfig(
        system_instructions=(
            "You are an operations assistant. Use the list_gcp_resources tool from "
            "the connected MCP server to answer questions about active GCP infrastructure."
        ),
        mcp_servers=mcp_servers,
    )
    result = await run_agent_workflow(config, payload.message)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@app.post("/api/chat/a2a")
async def chat_a2a(payload: ChatRequest):
    # Configure Supervisor agent that delegates to subagents
    config = LocalAgentConfig(
        system_instructions=(
            "You are a Supervisor Agent. Delegate complex subtasks to specialized "
            "subagents to fulfill the user request, then aggregate and return the final report."
        ),
        capabilities=types.CapabilitiesConfig(
            enable_subagents=True
        )
    )
    result = await run_agent_workflow(config, payload.message)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

# Serve index.html at root
@app.get("/")
async def get_index():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))

if __name__ == "__main__":
    import uvicorn
    # Verify API key is available
    if not os.environ.get("GEMINI_API_KEY"):
        print("WARNING: GEMINI_API_KEY environment variable is not set. Please set it or create a .env file.")
    print("Starting Web Testing Dashboard on http://127.0.0.1:8000")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
