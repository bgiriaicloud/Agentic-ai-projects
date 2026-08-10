# Enterprise Agentic AI Platform Demo (GCP Cloud Run & ADK)

This project demonstrates a production-ready, containerized **Agentic AI Platform** deployed on **Google Cloud Run** using the **Google Antigravity SDK (ADK)** and the **Model Context Protocol (MCP)**.

---

## 🚀 Architecture Diagram & Flow

```
  [User Browser] ──► [FastAPI Web Server] 
                             │
                             ▼ (ADK Orchestrator)
                       [Gemini LLM]
                             │
                             ▼ (Stdio Transport)
                       [FastMCP Server] ──► [External Knowledge Base]
```

1.  The client interacts with a glassmorphism web dashboard served by a **FastAPI** backend running on Google Cloud Run.
2.  The backend routes prompts to an **ADK Agent** powered by **Gemini** (`gemini-3.5-flash`).
3.  The agent establishes a local **Stdio Connection** to launch and communicate with a **FastMCP Server** (`mcp_server.py`).
4.  The MCP server queries an **External Knowledge Base** (mocked with production GCP networking, security, and deployment standards).
5.  The agent outputs reasoning steps (thoughts) and synthesizes the final grounded answer, which streams back to the UI.

---

## 📂 File Registry
*   `app.py`: FastAPI server serving the glassmorphic chat interface and exposing the `/api/chat` API endpoint.
*   `agent_run.py`: Google Antigravity SDK agent setup, configuring persona, system instructions, and connecting to the MCP server.
*   `mcp_server.py`: FastMCP server exposing GCP guidelines, architecture rules, and security compliance records.
*   `Dockerfile`: Secure, non-root multi-stage container configuration optimized for Google Cloud Run.
*   `requirements.txt`: Python package dependency registry.
*   `DEPLOYMENT_GUIDE.md`: Step-by-step instructions for deploying to Google Cloud Platform.

---

## 🛠️ Local Execution

### 1. Configure the Environment
Create a virtual environment and install the required dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up API Credentials
Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/api-keys) and export it:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Run the Server
Launch the FastAPI development server:
```bash
python3 app.py
```
Open your web browser and navigate to **`http://localhost:8080`** to chat with the agent.
