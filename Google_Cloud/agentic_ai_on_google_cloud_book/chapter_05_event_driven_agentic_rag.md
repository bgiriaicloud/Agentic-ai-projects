# Chapter 5: Event-Driven Agentic RAG on Google Cloud

> *"Agentic RAG elevates traditional retrieval by empowering the agent to formulate multi-queries, filter vector indices dynamically, and self-critique retrieved contexts for 100% groundedness."*

---

## 5.1 Event-Driven Pipeline Architecture

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           EVENT-DRIVEN AGENTIC RAG PIPELINE ON GCP                                │
├───────────────────────────────────────────────────────────────────────────────────────────────────┤
│  1. Ingress Layer   : Change Events (GCS Create, MySQL Binlog) ──> Google Cloud Pub/Sub           │
│  2. Streaming ETL   : Cloud Dataflow (Apache Beam) ──> Text Extraction & Layout Chunking          │
│  3. Embedding Model : Vertex AI Text Embeddings (text-embedding-004 / 768 or 3072 dims)           │
│  4. Data Lake Store : Google Cloud Storage (Bronze/Silver) & BigQuery Data Warehouse              │
│  5. Vector Search   : Vertex AI Vector Search (Matching Engine HNSW Index, Sub-50ms)              │
│  6. Agentic Brain   : Vertex AI Agent Builder + Gemini 2.0 (Hybrid Search + Grounded Synthesis)   │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5.2 Hybrid Search: Vector HNSW + Keyword BM25

To ensure high retrieval precision across both semantic concepts and exact keywords (like error codes or part numbers), enterprise RAG uses **Hybrid Search**:

```python
def compute_hybrid_rrf_score(vector_rank: int, keyword_rank: int, k: int = 60) -> float:
    """Computes Reciprocal Rank Fusion (RRF) score merging vector and keyword ranks."""
    return (1.0 / (k + vector_rank)) + (1.0 / (k + keyword_rank))
```

---

## 5.3 Vertex AI Vector Search (Matching Engine) Configuration

Vertex AI Vector Search utilizes **Hierarchical Navigable Small World (HNSW)** graph indexing:

```python
from google.cloud import aiplatform

def create_vertex_vector_index(project_id: str, location: str, display_name: str):
    """Provisions a Vertex AI Vector Search HNSW Index."""
    aiplatform.init(project=project_id, location=location)
    
    index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name=display_name,
        dimensions=768,
        approximate_neighbors_count=50,
        distance_measure_type="COSINE_DISTANCE",
        leaf_node_embedding_count=1000,
        leaf_nodes_to_search_percent=10,
        description="Enterprise HNSW Index for Agentic RAG Pipeline"
    )
    print(f"✅ Vertex AI Vector Search Index Created: {index.resource_name}")
```

---

## 5.4 Chapter Summary & Key Takeaways

* **Event-Driven Ingestion**: Real-time Pub/Sub streams trigger Dataflow chunking and Vertex AI vector upserts immediately upon document creation.
* **Hybrid Search**: Merging HNSW vector similarity with BM25 keyword matching via RRF prevents semantic misses.
* **Next Chapter**: In [Chapter 6](chapter_06_mcp_protocol_gcp_tools.md), we implement the **Model Context Protocol (MCP)** on Google Cloud.
