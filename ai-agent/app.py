import os
import asyncio
import streamlit as st
from multi_agent_architect import MultiAgentArchitect
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Multi-Agent ADK Orchestrator",
    page_icon="🤖",
    layout="wide"
)

# Custom dark glassmorphism styling
st.markdown("""
    <style>
        .stApp {
            background-color: #0b0f19;
            color: #f3f4f6;
        }
        .css-1542z7w {
            background-color: rgba(17, 25, 40, 0.7);
            backdrop-filter: blur(12px);
        }
    </style>
""", unsafe_allow_html=True)

st.title("Multi-Agent Supervisor Architecture (ADK) 🤖")
st.markdown("This dashboard demonstrates **Agent-to-Agent (A2A)** delegation using the **Google Antigravity SDK (ADK)** on Google Cloud Platform.")

# Dynamic workflow visualization
st.subheader("Multi-Agent Delegation Flow")
st.markdown("""
```
               ┌─────────────────────────────────┐
               │    Business User Requirement    │
               └────────────────┬────────────────┘
                                │
                                ▼
               ┌─────────────────────────────────┐
               │    Supervisor Agent (ADK)       │
               └───────┬──────────────────┬──────┘
                       │                  │
            (Delegate Sizing)      (Delegate Security)
                       ▼                  ▼
        ┌──────────────────────┐  ┌──────────────────────┐
        │  Cost Sizing Agent   │  │Security Sizing Agent │
        └──────────────┬───────┘  └───────┬──────────────┘
                       │                  │
                       └────────┬─────────┘
                                │ (Aggregate & Compile)
                                ▼
               ┌─────────────────────────────────┐
               │   Final Architecture Blueprint  │
               └─────────────────────────────────┘
```
""")

# Setup Sidebar example templates
st.sidebar.header("Architecture Requirements Templates")
template_choice = st.sidebar.selectbox(
    "Choose a sample requirements prompt:",
    [
        "Custom Configuration...",
        "Three-tier Web App on Cloud Run & Cloud SQL",
        "High-Availability GKE Cluster for Microservices",
        "Internal Data Lake with BigQuery & Cloud Storage"
    ]
)

default_prompt = ""
if template_choice == "Three-tier Web App on Cloud Run & Cloud SQL":
    default_prompt = (
        "We need a robust blueprint to host a production three-tier web application. "
        "The frontend runs on Google Cloud Run (3 instances expected). "
        "The backend database is hosted on Cloud SQL PostgreSQL. "
        "Task 1: Estimate monthly compute and database hosting expenses. "
        "Task 2: Define zero-trust security rules, private access requirements, and IAM access controls."
    )
elif template_choice == "High-Availability GKE Cluster for Microservices":
    default_prompt = (
        "We want to deploy a high-availability GKE cluster to run a microservices application. "
        "The cluster should run 5 worker nodes (e2-standard-4 instances). "
        "Task 1: Estimate compute resources and cluster management costs. "
        "Task 2: Outline network security taints/tolerations, Workload Identity bindings, and secrets management."
    )
elif template_choice == "Internal Data Lake with BigQuery & Cloud Storage":
    default_prompt = (
        "Design a secure corporate data lake. "
        "We will ingest raw transactional data into Cloud Storage buckets and copy it into BigQuery for analytics. "
        "Task 1: Estimate storage costs for 10TB of active files. "
        "Task 2: Detail Customer-Managed Encryption Keys (CMEK) via Cloud KMS, VPC Service Controls, and IAM viewer permissions."
    )

user_requirement = st.text_area(
    "Enter architectural requirements:", 
    value=default_prompt,
    placeholder="Describe your target GCP architecture, hosting load, and security compliance constraints...",
    height=150
)

if st.button("Synthesize Architecture Blueprint", type="primary"):
    if not user_requirement.strip():
        st.warning("Please specify architectural requirements first.")
    else:
        # Check API key presence
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            st.error("Error: GEMINI_API_KEY environment variable not found. Please add it to your .env file.")
        else:
            # Layout placeholders for real-time streaming updates
            thought_header = st.empty()
            thought_area = st.empty()
            
            blueprint_header = st.empty()
            blueprint_area = st.empty()
            
            # Instantiate A2A orchestrator
            architect = MultiAgentArchitect()
            
            # Capture streamed events
            thoughts = []
            final_text = []
            
            async def run_streaming_ui():
                async for event in architect.execute_workflow(user_requirement):
                    if event["type"] == "thought":
                        thoughts.append(event["content"])
                        thought_header.subheader("Supervisor Delegation & Reasoning Logs (ADK Thoughts)")
                        # Render cumulative thoughts inside code block to show execution path
                        thought_area.code("".join(thoughts), language="text")
                    elif event["type"] == "text":
                        final_text.append(event["content"])
                        blueprint_header.subheader("Final Synthesized GCP Architecture Blueprint")
                        blueprint_area.markdown("".join(final_text))
            
            # Execute async loop in streamlit context
            asyncio.run(run_streaming_ui())
