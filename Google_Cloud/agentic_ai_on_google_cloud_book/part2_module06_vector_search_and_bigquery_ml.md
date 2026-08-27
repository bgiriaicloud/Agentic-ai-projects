# Module 06: Core Data & Search Infrastructure: Vertex AI Vector Search & BigQuery ML

> *"Vertex AI Vector Search (formerly Matching Engine) delivers sub-50 millisecond vector retrieval over billions of embeddings, while BigQuery ML embeds SQL analytics into the heart of RAG pipelines."*

---

## 6.1 Vertex AI Vector Search (Matching Engine HNSW Index)

Vertex AI Vector Search is engineered with Google's proprietary **ScaNN (Scalable Nearest Neighbors)** and **HNSW (Hierarchical Navigable Small World)** indexing algorithms:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      VERTEX AI VECTOR SEARCH HNSW                      │
├────────────────────────────────────────────────────────────────────────┤
│  • Scale      : Supports billions of embeddings with 99.9% recall.     │
│  • Latency    : Sub-50ms p99 query latency under heavy concurrency.   │
│  • Filtering  : Boolean predicate filtering on metadata tags.          │
│  • Metrics    : Cosine Distance, Dot Product, Euclidean Distance (L2). │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6.2 BigQuery ML & Vector Integration

BigQuery enables running LLM embeddings and vector search directly using standard SQL queries:

```sql
-- Generate Vector Embeddings directly in BigQuery
SELECT * FROM ML.GENERATE_EMBEDDING(
  MODEL `my_project.my_dataset.text_embedding_model`,
  TABLE `my_project.my_dataset.enterprise_documents`,
  STRUCT(TRUE AS flatten_json_output)
);
```
