# Enterprise Agentic RAG Architecture & Planning Guide on Azure
## Multimodal Ingestion (SharePoint, Azure DevOps, GitHub) across Text, Code, PDF, PPTX & Images

This comprehensive guide presents an enterprise-grade architecture and implementation plan for building an **Agentic Retrieval-Augmented Generation (RAG)** platform on Microsoft Azure. It details multi-source ingestion, multimodal document extraction, custom chunking strategies, hybrid vector search with Entra ID security trimming, and agentic multi-query orchestration.

---

## 📋 Table of Contents
* [Section 1: Enterprise Agentic RAG Architecture Diagram](#section-1-enterprise-agentic-rag-architecture-diagram)
* [Section 2: Multi-Source Data Connectors & Security Trimming](#section-2-multi-source-data-connectors--security-trimming)
* [Section 3: Multimodal Document Extraction & OCR Pipeline](#section-3-multimodal-document-extraction--ocr-pipeline)
* [Section 4: Format-Specific Chunking & Embedding Strategies](#section-4-format-specific-chunking--embedding-strategies)
* [Section 5: Azure AI Search Vector Indexing & Hybrid Retrieval Engine](#section-5-azure-ai-search-vector-indexing--hybrid-retrieval-engine)
* [Section 6: Enterprise Agentic RAG Orchestration Workflow](#section-6-enterprise-agentic-rag-orchestration-workflow)
* [Section 7: Enterprise Governance, Observability & FinOps](#section-7-enterprise-governance-observability--finops)

---

## Section 1: Enterprise Agentic RAG Architecture Diagram

![Enterprise Azure Agentic RAG Architecture](file:///Users/biswanathgiri/.gemini/antigravity-ide/brain/9783c67e-1064-4e7d-8c3e-892122e2efed/enterprise_azure_agentic_rag_architecture_1787247973827.jpg)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 ENTERPRISE DATA SOURCES                                           │
│  ┌─────────────────────────┐   ┌───────────────────────────┐   ┌──────────────────────────────┐  │
│  │    SharePoint Online    │   │       Azure DevOps        │   │      GitHub Repositories     │  │
│  │ (.docx, .pdf, .pptx,    │   │ (Wikis, Work Items,       │   │ (Code, .md, issues,          │  │
│  │  images, site pages)    │   │  Boards, Git Repos)       │   │  pull requests, docs)        │  │
│  └────────────┬────────────┘   └─────────────┬─────────────┘   └──────────────┬───────────────┘  │
└───────────────┼──────────────────────────────┼────────────────────────────────┼───────────────────┘
                │                              │                                │
                ▼                              ▼                                ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               INGESTION & SECURITY TRIMMING LAYER                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  Microsoft Graph API / ADO REST API / GitHub Webhooks (Delta Sync + ACL Entra ID Fetch)    │  │
│  └───────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────┼────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           MULTIMODAL EXTRACTION & CHUNKING ENGINE                                 │
│  ┌─────────────────────────────────┐ ┌─────────────────────────────────┐ ┌───────────────────────┐ │
│  │ Azure AI Document Intelligence  │ │  Native AST Markdown/Code Parser│ │ GPT-4o Vision OCR     │ │
│  │ (PDF, DOCX, PPTX Layout & Tables)│ │ (Code classes, functions, .md)  │ │ (Architecture diagrams│ │
│  └────────────────┬────────────────┘ └────────────────┬────────────────┘ └───────────┬───────────┘ │
└───────────────────┼───────────────────────────────────┼──────────────────────────────┼─────────────┘
                    │                                   │                              │
                    └───────────────────────────────────┼──────────────────────────────┘
                                                        │
                                                        ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             EMBEDDING & VECTOR INDEXING LAYER                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  Azure OpenAI text-embedding-3-large (3072 dims) + Azure AI Search Vector Store             │  │
│  │  - HNSW Vector Index + BM25 Keyword Inverted Index + Entra ID Security ACL Filter           │  │
│  └───────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────┼────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               AGENTIC QUERY ORCHESTRATION LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  Master Supervisor Agent (Query Decomposition, Multi-Query Planning, Security Filter)       │  │
│  └───────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
│                                              │                                                    │
│               ┌──────────────────────────────┴──────────────────────────────┐                     │
│               ▼                                                             ▼                     │
│  ┌─────────────────────────┐                                 ┌─────────────────────────┐          │
│  │  L1 Hybrid Retrieval    │                                 │  L2 Semantic Reranker   │          │
│  │  (Vector + Keyword RRF) │ ──────────────────────────────> │  (Azure AI Search Ranker)│          │
│  └─────────────────────────┘                                 └────────────┬────────────┘          │
└───────────────────────────────────────────────────────────────────────────┼───────────────────────┘
                                                                            │
                                                                            ▼
                                                           ┌─────────────────────────────────┐
                                                           │  Grounded Synthesis & Answer    │
                                                           │  with Entra ID Trimming & Links │
                                                           └─────────────────────────────────┘
```

---

## Section 2: Multi-Source Data Connectors & Security Trimming

To satisfy enterprise compliance, data must be ingested securely while preserving original Access Control Lists (ACLs) so users can query ONLY documents they have read access to.

### 1. Data Source Connector Specification

| Source | Target Content Types | Ingestion Mechanism | Sync Frequency |
| :--- | :--- | :--- | :--- |
| **SharePoint Online** | `.docx`, `.pdf`, `.pptx`, `.html`, `.png`, `.jpg` | Microsoft Graph API v1.0 / Azure AI Search SharePoint Indexer | Delta Sync (Every 15 mins) |
| **Azure DevOps** | Wiki `.md`, Work Items, Project Boards, Repositories | Azure DevOps REST API / Webhooks | Real-time Event Webhook + Nightly Full Sync |
| **GitHub Repos** | `.md`, Source Code (`.py`, `.js`, `.cs`), Issues, PRs | GitHub GraphQL API v4 / Webhooks | Real-time Push Webhook |

### 2. Entra ID (Azure AD) Security Trimming Workflow

Security trimming prevents unauthorized data access during RAG retrieval:

```
[User Query + Entra ID User Token] ──> [Extract User Group SIDs (e.g., 'group-guid-123')]
                                                        │
                                                        ▼
[Azure AI Search Query] ──> Filter: "group_ids/any(g: g eq 'group-guid-123') or user_ids/any(u: u eq 'user-guid-456')"
                                                        │
                                                        ▼
                         [Only Security-Permitted Chunks Returned to LLM Context]
```

#### Code Snippet: Security-Trimmed Azure AI Search Query (Python)
```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

def search_with_security_trimming(
    search_client: SearchClient,
    query_text: str,
    query_vector: list,
    user_entra_id: str,
    user_group_sids: list
) -> list:
    """Executes Hybrid Vector Search with Entra ID Security Trimming."""
    
    # Format Entra ID security filter
    groups_filter = " or ".join([f"allowed_groups/any(g: g eq '{g}')" for g in user_group_sids])
    security_filter = f"allowed_users/any(u: u eq '{user_entra_id}') or ({groups_filter})"
    
    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=50,
        fields="text_vector"
    )
    
    results = search_client.search(
        search_text=query_text,
        vector_queries=[vector_query],
        filter=security_filter,  # SECURITY TRIMMING ENFORCEMENT
        top=10,
        select=["chunk_id", "title", "content", "source_url", "allowed_users"]
    )
    return [doc for doc in results]
```

---

## Section 3: Multimodal Document Extraction & OCR Pipeline

Enterprise files contain complex structural elements (tables, embedded architecture diagrams, slide decks) requiring format-aware extraction engines.

```
                  ┌───────────────────────────────────────────────┐
                  │          Incoming Source Document             │
                  └───────────────────────┬───────────────────────┘
                                          │
       ┌──────────────────────────────────┼──────────────────────────────────┐
       ▼                                  ▼                                  ▼
┌──────────────┐                  ┌──────────────┐                  ┌──────────────┐
│  PDF / DOCX  │                  │  PPTX Slides │                  │  PNG / JPG   │
└──────┬───────┘                  └──────┬───────┘                  └──────┬───────┘
       │                                  │                                  │
       ▼                                  ▼                                  ▼
┌─────────────────────────────┐    ┌─────────────────────────────┐    ┌─────────────────────────────┐
│ Azure AI Doc Intelligence   │    │ Slide-Level Text Extraction │    │ Azure OpenAI GPT-4o Vision  │
│ (Layout Model -> Markdown)  │    │ + Embedded Image OCR        │    │ (Image-to-Text Captioning)  │
└──────────────┬──────────────┘    └──────────────┬──────────────┘    └──────────────┬──────────────┘
               │                                  │                                  │
               └──────────────────────────────────┼──────────────────────────────────┘
                                                  │
                                                  ▼
                               ┌─────────────────────────────────────┐
                               │  Normalized Multimodal Markdown Text │
                               └─────────────────────────────────────┘
```

### Format Extraction Matrix

1.  **PDF & DOCX Files**: Processed via **Azure AI Document Intelligence (Layout Model)**. Converts complex multi-column layouts into standardized Markdown, preserving table structures as HTML/Markdown tables.
2.  **PPTX Presentation Decks**: Extracted per slide. Merges slide title, bullet points, speaker notes, and OCR descriptions of embedded charts into a single slide-level document chunk.
3.  **Images & Architecture Diagrams (`.png`, `.jpg`, `.svg`)**: Passed to **Azure OpenAI GPT-4o Vision** to synthesize descriptive textual captions (e.g., "Architecture diagram showing API Gateway connecting to Microservice A and Azure SQL").
4.  **Markdown (`.md`), HTML, & Text (`.txt`)**: Parsed natively using AST parsers to preserve code blocks, headers, and metadata tags.

---

## Section 4: Format-Specific Chunking & Embedding Strategies

Generic fixed-character chunking (e.g., splitting every 500 characters) destroys semantic relationships in code, tables, and presentation slides. We enforce **Format-Aware Dynamic Chunking**:

| File Format | Chunking Strategy | Target Chunk Size | Overlap | Semantic Boundary |
| :--- | :--- | :--- | :--- | :--- |
| **Markdown (`.md`)** | Header-Based Split | 800 - 1,200 Tokens | 100 Tokens | Split on `# H1`, `## H2`, `### H3` headings |
| **PDF & DOCX** | Layout & Table Block Split | 512 - 1,024 Tokens | 128 Tokens | Keep table structures whole in a single chunk |
| **PPTX Decks** | Slide-Level Granularity | 1 Slide per Chunk | 0 Tokens | Slide boundary + Speaker notes |
| **Source Code (`.py`, `.cs`)** | AST Code-Aware Split | 512 - 1,024 Tokens | 64 Tokens | Class / Function / Method boundaries |
| **Images & Diagrams** | Caption-Level Chunking | Full Image Caption | 0 Tokens | Single synthetic caption block |

### Vector Embedding Configuration

*   **Embedding Model**: Azure OpenAI `text-embedding-3-large`.
*   **Dimensions**: 3,072 dimensions (normalized for cosine similarity).
*   **Multimodal Embedding**: For raw images, use `multimodal-embedding` API to generate 1024-dimensional vectors stored in a secondary vector field.

---

## Section 5: Azure AI Search Vector Indexing & Hybrid Retrieval Engine

Azure AI Search acts as the central enterprise retrieval engine combining **L1 Hybrid Search** and **L2 Semantic Reranking**.

```json
{
  "name": "enterprise-agentic-rag-index",
  "fields": [
    { "name": "chunk_id", "type": "Edm.String", "key": true, "searchable": false },
    { "name": "source_type", "type": "Edm.String", "filterable": true, "facetable": true },
    { "name": "source_url", "type": "Edm.String", "searchable": false },
    { "name": "title", "type": "Edm.String", "searchable": true },
    { "name": "content", "type": "Edm.String", "searchable": true },
    { 
      "name": "text_vector", 
      "type": "Collection(Edm.Single)", 
      "searchable": true, 
      "dimensions": 3072, 
      "vectorSearchProfile": "my-hnsw-profile" 
    },
    { "name": "allowed_users", "type": "Collection(Edm.String)", "filterable": true },
    { "name": "allowed_groups", "type": "Collection(Edm.String)", "filterable": true }
  ],
  "vectorSearch": {
    "algorithms": [
      {
        "name": "my-hnsw-config",
        "kind": "hnsw",
        "hnswParameters": { "m": 4, "efConstruction": 400, "efSearch": 500, "metric": "cosine" }
      }
    ],
    "profiles": [
      { "name": "my-hnsw-profile", "algorithm": "my-hnsw-config" }
    ]
  },
  "semantic": {
    "configurations": [
      {
        "name": "my-semantic-config",
        "prioritizedFields": {
          "titleField": { "fieldName": "title" },
          "prioritizedContentFields": [{ "fieldName": "content" }]
        }
      }
    ]
  }
}
```

### Retrieval Pipeline Mechanics

1.  **L1 Keyword Search**: Runs standard BM25 inverted index query.
2.  **L1 Vector Search**: Runs HNSW similarity query using `text-embedding-3-large` query vector.
3.  **Reciprocal Rank Fusion (RRF)**: Merges keyword and vector rank positions into a single unified candidate list.
4.  **L2 Semantic Reranker**: Passes top 50 RRF candidate chunks to Azure's cross-encoder model, outputting refined semantic relevance scores (`@search.rerankerScore`).

---

## Section 6: Enterprise Agentic RAG Orchestration Workflow

The Agentic Orchestrator replaces traditional single-turn RAG with an iterative, multi-step reasoning loop.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Agentic Query Orchestrator Loop                      │
├────────────────────────────────────────────────────────────────────────┤
│  Step 1: User Query Intent & Scope Classification                     │
│          • Detects if query needs SharePoint, ADO, or GitHub data.     │
├────────────────────────────────────────────────────────────────────────┤
│  Step 2: Multi-Query Planning & Decomposition                         │
│          • Deconstructs "Compare PR 402 with SharePoint Arch doc"       │
│            into Query A (GitHub PR 402) & Query B (SharePoint Arch).   │
├────────────────────────────────────────────────────────────────────────┤
│  Step 3: Parallel Security-Trimmed Hybrid Retrieval                    │
│          • Executes concurrent queries against Azure AI Search         │
│            passing user's Entra ID SIDs.                              │
├────────────────────────────────────────────────────────────────────────┤
│  Step 4: Grounded Synthesis & Citation Validation                      │
│          • Verifies answer claims against retrieved context chunks.    │
│          • Formats inline citations: [SharePoint: Arch.pdf#Page3].     │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Section 7: Enterprise Governance, Observability & FinOps

### 1. Observability with Application Insights
*   **Metrics Tracked**: Ingestion lag, extraction failure rate, retrieval latency ($p95 < 800\text{ms}$), token consumption, and `@search.rerankerScore` distribution.
*   **Evaluation Metrics**: Groundedness score, Answer Relevance score, Context Precision.

### 2. FinOps & Cost Optimization
*   **Azure OpenAI Context Caching**: Cache system prompts and repetitive document context to reduce input token billing by up to 75%.
*   **Azure AI Search Sizing**: Utilize Standard S1/S2 partitions with auto-scaling to balance storage density and QPS throughput.
