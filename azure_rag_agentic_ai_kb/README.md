# Azure AI Search - Agentic Retrieval Demo & Implementation

This repository provides a complete, production-grade demo project for **Agentic Retrieval in Azure AI Search** based on the latest Microsoft Azure documentation ([Azure AI Search Agentic Retrieval Overview](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)).

---

## 🌟 What is Agentic Retrieval?

In **Azure AI Search**, *Agentic Retrieval* is a multi-query pipeline designed for complex questions posed by users or AI agents in chat and copilot applications. It underpins **Foundry IQ** in Microsoft Azure AI Foundry and powers advanced RAG (Retrieval-Augmented Generation) patterns.

### Key Capabilities
1. **Query Decomposition & Expansion**: Uses an LLM (e.g. `gpt-4o`) to break complex multi-part user queries into targeted subqueries.
2. **Context Resolution**: Incorporates conversation chat history to resolve ambiguous references and correct typos/synonyms.
3. **Parallel Multi-Query Execution**: Runs subqueries simultaneously across multiple knowledge sources (hybrid search, dense vector search, and BM25 keyword search).
4. **L2 Semantic Reranking**: Applies Azure AI Search's Semantic Reranker to score and rerank all retrieved document chunks.
5. **Answer Synthesis & Citations**: Synthesizes a grounded answer with inline citations (`[1]`, `[2]`), source references, and activity logs.

---

## 🏗 Architecture & Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│                      User / Agent Complex Query                  │
└─────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                Azure AI Search Knowledge Base                    │
└─────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│               1. Query Planner (Azure OpenAI LLM)                │
│    Decomposes multi-intent query into focused subqueries          │
└──────────────┬──────────────────┬──────────────────┬─────────────┘
               │                  │                  │
               ▼                  ▼                  ▼
┌──────────────────────┐┌──────────────────┐┌──────────────────────┐
│  Subquery 1 (Hotel)  ││Subquery 2(Shuttle││Subquery 3 (Vegetarian│
└──────────────┬───────┘└─────────┬────────┘└──────────┬───────────┘
               │                  │                    │
               ▼                  ▼                    ▼
┌──────────────────────┐┌──────────────────┐┌──────────────────────┐
│  Hotels Index        ││ Transport Index  ││ Dining Index         │
│  (Hybrid Search)     ││ (Vector Search)  ││ (Keyword Search)     │
└──────────────┬───────┘└─────────┬────────┘└──────────┬───────────┘
               │                  │                    │
               ▼                  ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│              2. L2 Semantic Reranker (Score Filtering)           │
└─────────────────────────────────┬────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│              3. Result Synthesis & Grounded Citations            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
azure_rag_agentic_ai_kb/
├── agentic_retrieval_engine.py   # Core Python Agentic Retrieval Engine & Cost Calculator
├── app.py                        # FastAPI Backend REST Server & API Payload Generator
├── test_engine.py                # Unit Test Suite for Pipeline Logic & Reranker Sorting
├── requirements.txt              # Python Dependencies
├── .env.example                  # Environment Configuration Template
├── README.md                     # Comprehensive Project Documentation
└── static/
    ├── index.html                # Glassmorphic Web Dashboard
    ├── style.css                 # Custom CSS Design System
    └── app.js                    # Interactive Frontend Application Logic
```

---

## 🚀 Quick Start (Simulated / Mock Mode)

No Azure credentials are required to try the demo locally out of the box!

### 1. Install Dependencies
```bash
cd azure_rag_agentic_ai_kb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Unit Tests
```bash
python3 test_engine.py
```

### 3. Launch Web Demo Application
```bash
python3 app.py
```
Open your browser and navigate to: **`http://localhost:8000`**

---

## ⚡ Connecting to Live Azure Services

To connect to your live Azure AI Search and Azure OpenAI resources:

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Update `.env` with your Azure details:
   ```ini
   AZURE_SEARCH_SERVICE_ENDPOINT=https://<your-search-service>.search.windows.net
   AZURE_SEARCH_ADMIN_KEY=<your-azure-search-key>
   AZURE_SEARCH_API_VERSION=2026-05-01-preview

   AZURE_OPENAI_ENDPOINT=https://<your-openai-resource>.openai.azure.com
   AZURE_OPENAI_API_KEY=<your-azure-openai-key>
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

   EXECUTION_MODE=azure
   ```

---

## 📡 Native Azure AI Search REST API Specification (`2026-05-01-preview`)

### Retrieve Action Payload Example

```http
POST https://<search-service>.search.windows.net/knowledgebases/kb-agentic/retrieve?api-version=2026-05-01-preview
Content-Type: application/json
api-key: [YOUR_AZURE_SEARCH_ADMIN_KEY]

{
  "query": "Find me a hotel near the beach, with airport transportation, and near vegetarian restaurants",
  "reasoningEffort": "low",
  "conversationHistory": [],
  "options": {
    "includeActivityLog": true,
    "includeCitations": true,
    "semanticReranking": "enabled",
    "top": 5
  }
}
```

---

## 📊 Token Usage & Cost Estimation Formula

Following official Microsoft billing guidelines:
- **Azure OpenAI**: Billed for Query Planning input/output tokens (using `gpt-4o-mini` or `gpt-4o` rates).
- **Azure AI Search**: Billed per token evaluated during L2 Semantic Reranking ($\approx 500 \text{ tokens} \times \text{chunks reranked}$).

$$\text{Total Cost} = (\text{OpenAI Input Tokens} \times \$0.15/\text{M}) + (\text{OpenAI Output Tokens} \times \$0.60/\text{M}) + (\text{Rerank Tokens} \times \$0.022/\text{M})$$

---

## 📜 References & Further Reading
- [Microsoft Learn: Agentic Retrieval in Azure AI Search Overview](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview)
- [Microsoft Learn: Build an End-to-End Agentic Retrieval Solution](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-pipeline)
