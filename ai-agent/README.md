# Multi-Agent Supervisor Architecture (ADK)

This project demonstrates a **Multi-Agent Supervisor Architecture** utilizing the **Google Antigravity SDK (ADK)**. It showcases **Agent-to-Agent (A2A)** delegation, where a central Supervisor Agent dynamically spawns, manages, and aggregates outputs from specialized worker agents to solve complex cloud deployment problems.

---

## 🚀 Architectural Pattern

```
               ┌───────────────────────────────┐
               │         Business User         │
               └───────────────┬───────────────┘
                               │ (Requirement)
                               ▼
               ┌───────────────────────────────┐
               │    Supervisor Agent (ADK)     │
               └───────┬───────────────┬───────┘
                       │               │
        ┌──────────────┴──────┐ ┌──────┴──────────────┐
        │  Cost Sizing Agent  │ │Security Sizing Agent│
        └─────────────────────┘ └─────────────────────┘
```

1.  The User describes their application footprint (e.g. compute load, database instances, compliance guidelines).
2.  The **Supervisor Agent** (Senior Cloud Architect) receives the request and splits it into independent cost estimation and security audit subtasks.
3.  It spawns a **Cost Sizing Subagent** and a **Security Sizing Subagent** dynamically.
4.  Each subagent solves its specific task and returns its findings to the Supervisor.
5.  The Supervisor synthesizes the outputs into a single, cohesive deployment blueprint, displaying it on the Streamlit UI.

---

## 📂 File Registry
*   `app.py`: Streamlit frontend dashboard visualising the delegation flow, streaming agent thoughts, and rendering the final aggregated report.
*   `multi_agent_architect.py`: Python module defining the `MultiAgentArchitect` class, which initializes the ADK Supervisor Agent with `enable_subagents=True`.
*   `requirements.txt`: Python package registry.
*   `.env`: Local environment configuration variables file.
*   `.env.example`: Configuration template.

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
Configure your Gemini API key inside the `.env` file:
```env
GEMINI_API_KEY="your-api-key-here"
```

### 3. Run the Streamlit Dashboard
Launch the dashboard:
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser to interact with the multi-agent system.
