# Conversational Analytics Data Agent (Streamlit & BigQuery)

This project implements a **Conversational Analytics Data Agent** that allows users to query Google Cloud BigQuery public datasets in plain English, generates SQL queries dynamically, executes them, and visualizes the results on an interactive dashboard.

It matches the exact architecture described in the **Conversational Analytics API** system design:

```
  [Business User] ──► [Streamlit App] ──► [Vertex AI/Gemini (ADK)]
                             ▲                     │
                             │ (JSON Data)         ▼ (Generated SQL)
                             └────────────── [BigQuery Database]
```

---

## 📂 File Registry
*   `app.py`: Streamlit front-end dashboard that takes user prompts, triggers the agent, displays the SQL, and renders data grids and charts.
*   `agentic_bigquery.py`: Google Antigravity SDK (ADK) agent definition containing system instructions, DB schemas (grounding rules), and BigQuery connection tools.
*   `requirements.txt`: Python package dependencies registry.
*   `DEPLOYMENT_GUIDE.md`: Manual for deploying the Streamlit app on GCP Cloud Run.
*   `.env`: Local environment settings file.
*   `.env.example`: Template for environment setup.

---

## 🛠️ Local Execution

### 1. Configure the Environment
Create a virtual environment and install the required dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure GCP Credentials & API Keys
Make sure you have authenticated your local session to Google Cloud to query BigQuery:
```bash
gcloud auth application-default login
```
Create a `.env` file and configure your API key:
```env
GEMINI_API_KEY="your-api-key-here"
GCP_PROJECT_ID="your-gcp-project-id"
```

### 3. Launch the Streamlit App
Run the Streamlit application locally:
```bash
streamlit run app.py
```
Open your web browser and navigate to the printed address (default: **`http://localhost:8501`**).
