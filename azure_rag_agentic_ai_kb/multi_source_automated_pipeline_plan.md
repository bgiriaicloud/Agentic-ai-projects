# Multi-Source Automated Real-Time Event Pipeline for Azure Agentic RAG
## SharePoint Online, Azure DevOps, and GitHub Repositories

This guide presents an enterprise architecture and implementation plan for a **Multi-Source Real-Time Ingestion Pipeline** on Azure. It listens to native webhooks from **SharePoint Online**, **Azure DevOps**, and **GitHub Repositories**, automatically reflecting file creations, updates, and deletions (`.md`, `.pdf`, `.docx`) in **Azure AI Search** within seconds.

---

## 📋 Table of Contents
* [Section 1: Multi-Source Automated Architecture Diagram](#section-1-multi-source-automated-architecture-diagram)
* [Section 2: Native Webhook Configurations per Source](#section-2-native-webhook-configurations-per-source)
* [Section 3: Unified Event Dispatcher & Normalization Engine](#section-3-unified-event-dispatcher--normalization-engine)
* [Section 4: Automated Index Upsert & Delete Synchronization](#section-4-automated-index-upsert--delete-synchronization)

---

## Section 1: Multi-Source Automated Architecture Diagram

![Multi-Source Real-Time Event-Driven RAG Architecture](file:///Users/biswanathgiri/.gemini/antigravity-ide/brain/9783c67e-1064-4e7d-8c3e-892122e2efed/multi_source_automated_event_rag_architecture_1787248537127.jpg)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   ENTERPRISE WEBHOOK EMITTERS                                     │
│  ┌─────────────────────────┐   ┌───────────────────────────┐   ┌──────────────────────────────┐  │
│  │    SharePoint Online    │   │       Azure DevOps        │   │      GitHub Repositories     │  │
│  │  (Microsoft Graph API   │   │   (ADO Service Hooks      │   │   (GitHub Webhooks           │  │
│  │   /subscriptions)       │   │    git.push, wiki.updated)│   │    push, gollum, PR)         │  │
│  └────────────┬────────────┘   └─────────────┬─────────────┘   └──────────────┬───────────────┘  │
└───────────────┼──────────────────────────────┼────────────────────────────────┼───────────────────┘
                │                              │                                │
                ▼                              ▼                                ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                UNIFIED EVENT DISPATCHER LAYER                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  Azure Event Grid / Azure Function Webhook Endpoint                                         │  │
│  │  - Normalizes webhooks into Unified Event Format: { source, action, file_path, doc_id }    │  │
│  └───────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────┼────────────────────────────────────────────────────┘
                                               │
               ┌───────────────────────────────┴───────────────────────────────┐
               ▼                                                               ▼
    [Action: Created / Updated]                                        [Action: Deleted]
               │                                                               │
               ▼                                                               ▼
┌─────────────────────────────────────────────┐             ┌─────────────────────────────────────┐
│ 1. Stream File Content (.md, .pdf, .docx)   │             │ 1. Query Azure AI Search Index for  │
│ 2. Extract Layout + GPT-4o Vision PDF OCR   │             │    all Chunks matching 'doc_id'     │
│ 3. Format-Aware Dynamic Chunking            │             │ 2. Execute Batch Purge              │
│ 4. text-embedding-3-large Vectorization     │             │    ('delete' action) in Index        │
└──────────────────────┬──────────────────────┘             └──────────────────┬──────────────────┘
                       │                                                       │
                       ▼                                                       ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               AZURE AI SEARCH VECTOR INDEX STORE                                  │
│  ┌─────────────────────────────────┐                     ┌─────────────────────────────────┐  │
│  │ Atomic Index Upsert             │                     │ Immediate Index Deletion        │  │
│  │ ('mergeOrUpload' batch)         │                     │ ('delete' batch)                │  │
│  └─────────────────────────────────┘                     └─────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Section 2: Native Webhook Configurations per Source

### 1. SharePoint Online: Microsoft Graph Webhooks
*   **API Endpoint**: `POST https://graph.microsoft.com/v1.0/subscriptions`
*   **Resource**: `sites/{site-id}/drives/{drive-id}/root`
*   **Change Types**: `created`, `updated`, `deleted`
*   **Lifecycle**: Auto-renewed via Azure Function timer before 3-day expiration.

### 2. Azure DevOps: Service Hooks
*   **Event Types**:
    *   `git.push` (Triggered on repository commit pushing `.md`, `.pdf`, or `.docx` updates).
    *   `wiki.page.updated` / `wiki.page.deleted` (Triggered on DevOps Wiki edits).
    *   `workitem.updated` (Triggered on Board Work Item edits).
*   **Target Payload**: HTTP POST to Azure Function Webhook Receiver.

### 3. GitHub Repositories: GitHub Webhooks
*   **Event Types**:
    *   `push` (Fires on `git push` modifying files).
    *   `gollum` (Fires on GitHub Wiki page edits).
    *   `pull_request` (Fires when PRs updating docs/code are merged into main).
*   **Security**: HMAC SHA-256 Signature verification using `X-Hub-Signature-256`.

---

## Section 3: Unified Event Dispatcher & Normalization Engine

The Azure Function Webhook Receiver normalizes payloads from all 3 platforms into a single unified JSON schema:

```json
{
  "source_system": "sharepoint | azure_devops | github",
  "event_action": "created | updated | deleted",
  "file_path": "docs/architecture_spec.pdf",
  "document_id": "sharepoint-drive-item-99812",
  "commit_sha": "a1b2c3d4",
  "timestamp": "2026-08-20T23:24:00Z"
}
```

---

## Section 6: Azure Cosmos DB: Is It Needed for Enterprise Agentic RAG?

### 1. Component Role Division: Azure AI Search vs. Azure Cosmos DB

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

### 2. Decision Matrix: When to Include Azure Cosmos DB

| Feature Requirement | Require Cosmos DB? | Architectural Rationale |
| :--- | :--- | :--- |
| **Single-Turn Q&A RAG Bot** | ❌ **NOT Needed** | Azure AI Search is sufficient for vector retrieval. |
| **Multi-Turn Chat History & Memory** | 🟢 **NEEDED** | Stores user session chat history documents with $<10\text{ms}$ multi-region SLA. |
| **Agentic State Machine & Memory** | 🟢 **NEEDED** | Stores supervisor agent tool execution logs, task checkpoints, and scratchpad memory. |
| **Ingestion Pipeline Audit & Sync Lineage** | 🟢 **NEEDED** | Tracks file processing state (`PENDING`, `COMPLETED`, `FAILED`, `FILE_HASH`) across SharePoint/ADO/GitHub. |
| **Integrated Vector Search on NoSQL Data** | 🟢 **OPTIONAL** | Native DiskANN / IVFFlat vector indexing on Cosmos DB NoSQL documents. |


