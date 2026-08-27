# Master Enterprise Agentic RAG Architecture Blueprint (Azure)
## End-to-End Multimodal Ingestion, Event Pipelines, Vector Search, State Management & Web Application

This document provides the definitive, production-grade **Master Reference Architecture** for an Enterprise Agentic RAG Platform on Microsoft Azure. It unifies all enterprise data sources, security boundaries, asynchronous message queues, document processing engines, vector stores, stateful NoSQL databases, and agentic orchestration layers into a cohesive blueprint.

---

## 📋 Table of Contents
* [Section 1: Master Architecture Diagram](#section-1-master-architecture-diagram)
* [Section 2: System Component Directory & Specification](#section-2-system-component-directory--specification)
* [Section 3: End-to-End Ingestion & Processing Data Flow](#section-3-end-to-end-ingestion--processing-data-flow)
* [Section 4: Database Role Division (AI Search vs. Cosmos DB)](#section-4-database-role-division-ai-search-vs-cosmos-db)
* [Section 5: Security Trimming & Entra ID Access Control](#section-5-security-trimming--entra-id-access-control)
* [Section 6: Production Sizing, SLA & Operational Cost Matrix](#section-6-production-sizing-sla--operational-cost-matrix)

---

## Section 1: Master Architecture Diagram

![Master Enterprise Azure Agentic RAG Architecture](file:///Users/biswanathgiri/.gemini/antigravity-ide/brain/9783c67e-1064-4e7d-8c3e-892122e2efed/multi_source_automated_event_rag_architecture_1787248537127.jpg)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       1. ENTERPRISE DATA SOURCES                                                  │
│   ┌───────────────────────────┐      ┌───────────────────────────┐      ┌──────────────────────────────────────┐  │
│   │     SharePoint Online     │      │       Azure DevOps        │      │         GitHub Repositories          │  │
│   │ (.docx, .pdf, .html,      │      │ (Wikis, Work Items,       │      │ (Source Code, .md, issues,           │  │
│   │  site pages, images)      │      │  Boards, Git Repos)       │      │  pull requests, docs)                │  │
│   └─────────────┬─────────────┘      └─────────────┬─────────────┘      └──────────────────┬───────────────────┘  │
└─────────────────┼──────────────────────────────────┼───────────────────────────────────────┼──────────────────────┘
                  │ (Graph Webhook)                  │ (ADO Service Hook)                    │ (GitHub Webhook)
                  ▼                                  ▼                                       ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 2. INGESTION, BUFFER & EVENT DISPATCHER LAYER                                     │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│   │  Azure App Service (Fast Webhook Receiver Endpoint)                                                         │  │
│   │  • Validates Entra ID / HMAC Signatures & Returns 200 OK (<100ms) to prevent emitter timeouts.              │  │
│   └─────────────────────────────────────────────────────┬──────────────────────────────────────────────────────┘  │
│                                                         │                                                         │
│                                                         ▼                                                         │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│   │  Azure Service Bus Queue & Dead-Letter Queue (DLQ)                                                         │  │
│   │  • Buffers incoming events, throttles spike spikes (prevents 429 errors), and manages 10x retries.         │  │
│   └─────────────────────────────────────────────────────┬──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┘
                                                          │
                                                          ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               3. MULTIMODAL EXTRACTION & PROCESSING PIPELINE                                      │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│   │  Azure Functions (Worker Processing Engine) & Azure Blob Storage (Document Staging)                       │  │
│   │  • Downloads document bytes, tracks ingestion hash state, and dispatches to extraction drivers:           │  │
│   │    1. Azure AI Document Intelligence Layout Model: Parses PDF & DOCX text, headers, & tables.             │  │
│   │    2. Azure OpenAI GPT-4o Vision OCR: Captures embedded PDF/DOCX figures, charts, & diagrams.              │  │
│   │    3. AST Markdown Parser: Header-based (# H1, ## H2) semantic chunking for .md & code files.              │  │
│   │    4. Azure OpenAI text-embedding-3-large: Generates 3072-dimensional normalized vector embeddings.        │  │
│   └─────────────────────────────────────────────────────┬──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┘
                                                          │
                                      ┌───────────────────┴───────────────────┐
                                      ▼                                       ▼
┌───────────────────────────────────────────────────────────┐   ┌───────────────────────────────────────────────────┐
│              4A. AZURE AI SEARCH                          │   │             4B. AZURE COSMOS DB                   │
│         (Vector Store & Search Index)                     │   │   (State, Memory & Audit Catalog Store)           │
├───────────────────────────────────────────────────────────┤   ├───────────────────────────────────────────────────┤
│ • HNSW Vector Index (3072 dims, Cosine metric)            │   │ • Multi-Turn User Chat Conversation Memory (<10ms)│
│ • BM25 Inverted Keyword Search Index                      │   │ • Supervisor Agent Task State Machine & Scratchpad│
│ • Reciprocal Rank Fusion (RRF) Hybrid Search              │   │ • Ingestion Sync Audit Catalog & Hash Lineage     │
│ • L2 Semantic Reranker (@search.rerankerScore)            │   │ • Document Versioning & Sync Lineage Tracking     │
│ • Entra ID ACL Security Trimming Filter                   │   │                                                   │
└─────────────────────────────┬─────────────────────────────┘   └─────────────────────────────┬─────────────────────┘
                              │                                                               │
                              └───────────────────────────────┬───────────────────────────────┘
                                                              │
                                                              ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              5. AGENTIC ORCHESTRATION & USER INTERFACE LAYER                                      │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│   │  Azure OpenAI Service (GPT-4o) Agentic Query Orchestrator                                                  │  │
│   │  • Query Intent Classification & Multi-Query Planning                                                      │  │
│   │  • Concurrent Security-Trimmed Parallel Retrieval against Azure AI Search                                  │  │
│   │  • Conversational Memory Retrieval & State Updates against Azure Cosmos DB                                 │  │
│   │  • Grounded Answer Synthesis with Inline Markdown Source Citations                                         │  │
│   └─────────────────────────────────────────────────────┬──────────────────────────────────────────────────────┘  │
│                                                         │                                                         │
│                                                         ▼                                                         │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│   │  Azure App Service (FastAPI / Interactive Glassmorphic Web App UI) & Application Insights Telemetry         │  │
│   └────────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Section 2: System Component Directory & Specification

| # | System Component | Azure Resource Type | Primary Responsibility in Architecture |
| :--- | :--- | :--- | :--- |
| **1** | **SharePoint Online** | Microsoft 365 Tenant | External document source (`.docx`, `.pdf`, `.html`, images, site pages). |
| **2** | **Azure DevOps** | Azure DevOps Services | External developer source (Wikis, Work Items, Boards, Git Repos). |
| **3** | **GitHub Repos** | GitHub Enterprise | External source code & documentation (`.md`, source code, issues, PRs). |
| **4** | **Webhook Receiver** | Azure App Service / Function | Validates incoming webhooks and returns immediate `200 OK` ($<100\text{ms}$). |
| **5** | **Event Buffer Queue** | Azure Service Bus Queue | Buffers messages, throttles burst spikes, and manages Dead-Letter Queue (DLQ). |
| **6** | **Enterprise Data Lake**| Azure Blob / ADLS Gen2 | Central Medallion Store (`raw-landing`, `extracted-curated`, `vector-payloads`). |
| **7** | **Async Worker Engine**| Azure Functions (Python) | Serverless execution worker for document parsing, chunking, and embedding. |
| **8** | **Document OCR Engine**| Azure AI Document Intelligence | Layout Model for PDF/DOCX structural parsing and HTML table extraction. |
| **9** | **Vision OCR Engine**  | Azure OpenAI GPT-4o Vision | Captures embedded PDF/DOCX figures, charts, and architectural diagrams. |
| **10**| **Vector Search Engine**| Azure AI Search (S1/S2 Tier) | Hybrid Search (HNSW + BM25 + L2 Semantic Reranker) & ACL Security Trimming. |
| **11**| **State & Memory Store**| Azure Cosmos DB (NoSQL API) | Multi-turn chat history ($<10\text{ms}$), Agent state machine, Ingestion audit catalog. |
| **12**| **Agent Orchestrator** | Azure OpenAI Service (GPT-4o) | Multi-query planning, tool calling, grounded answer synthesis with citations. |
| **13**| **Web Application UI** | Azure App Service (FastAPI) | User-facing chat interface with Application Insights observability telemetry. |

---

## Section 2B: Azure Data Lake Storage Gen2 (ADLS Gen2) Medallion Architecture

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                    AZURE DATA LAKE STORAGE GEN2 (ADLS GEN2) MEDALLION STORE                       │
│                                                                                                   │
│   ┌────────────────────────┐      ┌────────────────────────┐      ┌───────────────────────────┐   │
│   │    BRONZE CONTAINER    │      │    SILVER CONTAINER    │      │      GOLD CONTAINER       │   │
│   │    (raw-landing)       │      │   (extracted-curated)  │      │  (vector-chunk-payloads)  │   │
│   ├────────────────────────┤  ──> ├────────────────────────┤  ──> ├───────────────────────────┤   │
│   │ Raw file replicas from │      │ Extracted Markdown,    │      │ Clean JSON chunks & 3072  │   │
│   │ SharePoint, ADO, &     │      │ HTML tables, & GPT-4o  │      │ dim vectors ready for     │   │
│   │ GitHub (.pdf/.docx/.md)│      │ Vision OCR captions.   │      │ Azure AI Search upsert.   │   │
│   └────────────────────────┘      └────────────────────────┘      └───────────────────────────┘   │
│                                                                                                   │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    QUARANTINE / DEAD-LETTER CONTAINER (quarantine-dlq)                                    │   │
│   │    Stores failed OCR documents & malformed PDFs routed from Azure Service Bus DLQ.        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Medallion Container Roles:
*   **Bronze (`raw-landing`)**: Immutable raw file storage preserving original document bytes synced from SharePoint, Azure DevOps, and GitHub.
*   **Silver (`extracted-curated`)**: Stores clean, extracted Markdown text, HTML tables, and GPT-4o Vision OCR captions generated by Azure AI Document Intelligence. Allows high-speed batch re-indexing if embedding models upgrade without needing to re-fetch raw files.
*   **Gold (`vector-chunk-payloads`)**: Stores formatted vector chunk payloads (3072-dim vectors + metadata) matching Azure AI Search documents.
*   **Quarantine (`quarantine-dlq`)**: Quarantine container holding malformed documents or unresolvable extraction payloads for engineering review.

---

### 1. File Upload / Modification Flow
1.  **Event Emission**: User uploads `arch_spec.pdf` to SharePoint, pushes a `.md` commit to GitHub, or updates an Azure DevOps Wiki.
2.  **Webhook Trigger**: Emitter sends HTTP POST webhook to **Azure App Service Webhook Receiver**.
3.  **Instant ACK**: Webhook Receiver validates signature and returns `200 OK` ($<100\text{ms}$) to prevent timeout.
4.  **Service Bus Enqueue**: Receiver enqueues JSON message into **Azure Service Bus Queue**.
5.  **Worker Processing**: **Azure Function Worker** dequeues message (max 5 concurrent batch size).
6.  **Multimodal Extraction**:
    *   `Document Intelligence` extracts PDF layout and table structure.
    *   `GPT-4o Vision` processes embedded figure images, injecting `[FIGURE_CAPTION: ...]` inline.
7.  **Vectorization & Storage**:
    *   Generates 3072-dim embeddings via `text-embedding-3-large`.
    *   Executes `mergeOrUpload` batch upsert into **Azure AI Search**.
    *   Writes ingestion sync record (file hash, timestamp) to **Azure Cosmos DB**.

### 2. File Deletion Flow
1.  **Event Emission**: File deleted in SharePoint / ADO / GitHub.
2.  **Webhook Trigger**: Emitter sends `deleted` event webhook to Receiver.
3.  **Service Bus Enqueue**: Enqueues deletion job.
4.  **Batch Index Purge**: Worker queries **Azure AI Search** for all chunks matching `document_id` and executes atomic `delete` batch array.
5.  **Audit Update**: Updates **Azure Cosmos DB** sync status to `DELETED`.

---

## Section 4: Database Role Division (AI Search vs. Cosmos DB)

```
┌─────────────────────────────────────────┐       ┌─────────────────────────────────────────┐
│         AZURE AI SEARCH                 │       │          AZURE COSMOS DB                │
│  (Vector Store & Search Index)          │       │  (Agent Memory & State Persistence)     │
├─────────────────────────────────────────┤       ├─────────────────────────────────────────┤
│ • Stores Text Chunks & Vector Embeddings│       │ • Stores Multi-Turn Chat Conversation   │
│ • HNSW Similarity Search & BM25 Keyword │       │   History per User Session (<10ms SLA) │
│ • L2 Semantic Reranker (@rerankerScore) │       │ • Stores Agent Task State & Scratchpad  │
│ • Hybrid Reciprocal Rank Fusion (RRF)   │       │ • Stores Document Sync Lineage & Hashes │
└─────────────────────────────────────────┘       └─────────────────────────────────────────┘
```

---

## Section 5: Security Trimming & Entra ID Access Control

To enforce strict enterprise compliance, search queries filter candidate vector chunks based on the querying user's **Entra ID (Azure AD) Security Identifiers (SIDs)**:

```python
# Entra ID Security-Trimmed Query Execution
security_filter = f"allowed_users/any(u: u eq '{user_entra_id}') or allowed_groups/any(g: g eq '{group_sid_1}')"

results = search_client.search(
    search_text=query_text,
    vector_queries=[vector_query],
    filter=security_filter,  # Security Trimming Filter
    top=10
)
```

---

## Section 6: Production Sizing, SLA & Operational Cost Matrix

| Azure Service | Recommended Tier | SLA Target | Estimated Monthly Cost (USD) |
| :--- | :--- | :--- | :--- |
| **Azure AI Search** | Standard S1 (3 Search Units) | 99.9% Uptime | ~$750 / month |
| **Azure OpenAI Service** | Provisioned Throughput / Pay-Go | 99.9% Uptime | Variable (per token) |
| **Azure Cosmos DB** | Autoscale (400 - 4000 RU/s) | 99.999% Uptime | ~$150 / month |
| **Azure Service Bus** | Standard Tier | 99.9% Uptime | ~$10 / month |
| **Azure App Service** | Premium v3 (P1v3) | 99.95% Uptime | ~$85 / month |
| **Azure Functions** | Premium Plan (EP1) | 99.95% Uptime | ~$160 / month |
