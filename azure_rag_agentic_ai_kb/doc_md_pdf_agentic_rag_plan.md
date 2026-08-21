# Enterprise Agentic RAG Architecture & Planning Guide: .MD, .PDF, and .DOCX Focus

This guide presents a streamlined, production-ready **Agentic RAG Platform on Azure** designed specifically for **`.md` (Markdown)**, **`.pdf` (PDF Documents)**, and **`.docx` (Microsoft Word)** file formats. It includes an automated pipeline for extracting and captioning **embedded images, charts, and diagrams inside PDF files** using Azure OpenAI GPT-4o Vision.

---

## 📋 Table of Contents
* [Section 1: Focused RAG Architecture Overview](#section-1-focused-rag-architecture-overview)
* [Section 2: Format-Specific Processing & Embedded PDF Image Strategy](#section-2-format-specific-processing--embedded-pdf-image-strategy)
* [Section 3: Dynamic Chunking Matrix for .MD, .PDF, & .DOCX](#section-3-dynamic-chunking-matrix-for-md-pdf--docx)
* [Section 4: Azure AI Search Vector Index Schema](#section-4-azure-ai-search-vector-index-schema)
* [Section 5: Agentic Multi-Query Retrieval Workflow](#section-5-agentic-multi-query-retrieval-workflow)

---

## Section 1: Focused RAG Architecture Overview

![Focused .MD, .PDF, .DOCX RAG Architecture](file:///Users/biswanathgiri/.gemini/antigravity-ide/brain/9783c67e-1064-4e7d-8c3e-892122e2efed/focused_pdf_docx_md_rag_architecture_1787248209474.jpg)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               Target Enterprise Document Ingestion                                │
│   ┌──────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────────────┐  │
│   │    Markdown (.md) Files  │   │     PDF (.pdf) Files     │   │      Word (.docx) Files      │  │
│   │   (Headers, Code Blocks) │   │ (Text, Tables, Diagrams) │   │     (Headings, Paragraphs)   │  │
│   └────────────┬─────────────┘   └────────────┬─────────────┘   └──────────────┬───────────────┘  │
└────────────────┼──────────────────────────────┼────────────────────────────────┼───────────────────┘
                 │                              │                                │
                 ▼                              ▼                                ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               FORMAT-AWARE EXTRACTION & VISION OCR                                │
│  ┌──────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────────────────┐  │
│  │   AST Markdown Parser    │   │ Azure AI Doc Intelligence│   │ python-docx Layout Parser    │  │
│  │ (Splits on # H1, ## H2)  │   │  (Layout Model Extraction│   │  (Paragraphs & Tables)       │  │
│  └─────────────┬────────────┘   └─────────────┬────────────┘   └──────────────┬───────────────┘  │
│                │                              │                               │                  │
│                │                ┌─────────────┴─────────────┐                 │                  │
│                │                │  Embedded Image Extractor │                 │                  │
│                │                │  (GPT-4o Vision Captioning)                 │                  │
│                │                └─────────────┬─────────────┘                 │                  │
│                └──────────────────────────────┼───────────────────────────────┘                  │
└───────────────────────────────────────────────┼──────────────────────────────────────────────────┘
                                                │
                                                ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              DYNAMIC CHUNKING & EMBEDDING ENGINE                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  Format-Aware Chunker (Preserves Tables & Image Captions inside Text Chunks)               │  │
│  │  Azure OpenAI text-embedding-3-large (3072 Dimensions)                                     │  │
│  └───────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────┼────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               AZURE AI SEARCH VECTOR INDEX STORE                                  │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  HNSW Vector Index + BM25 Keyword Search + L2 Semantic Reranker (@search.rerankerScore)    │  │
│  └───────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────┼────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               AGENTIC QUERY ORCHESTRATION LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │  Agentic Multi-Query Planner (Decomposes User Query -> Parallel Hybrid Search -> Synthesis) │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Section 2: Format-Specific Processing & Embedded PDF Image Strategy

### 1. Embedded PDF Image & Diagram Handling Strategy

PDF files in enterprise repositories (whitepapers, architecture specs, financial reports) frequently contain critical embedded images, charts, and architectural diagrams.

```
[PDF Document Page] ──> Azure AI Doc Intelligence (Detects Figure Bounding Box)
                                 │
                                 ▼
                     [Crop Embedded Figure Image]
                                 │
                                 ▼
                [Azure OpenAI GPT-4o Vision API]
                                 │
                                 ▼
       [Generated Text Caption: "[EMBEDDED_DIAGRAM: Architecture showing...]"]
                                 │
                                 ▼
            [Injected Directly Into Corresponding Text Chunk]
```

*   **Step 1: Figure Detection**: Azure AI Document Intelligence Layout Model parses PDF pages and returns `figures` bounding box coordinates.
*   **Step 2: Image Crop & Extraction**: The pipeline crops the embedded image bytes from the PDF page.
*   **Step 3: GPT-4o Vision Captioning**: Passes the cropped image to Azure OpenAI GPT-4o Vision with a targeted prompt: *"Describe this technical architecture diagram or data chart in detail for search indexing."*
*   **Step 4: Chunk Injection**: Embeds the generated description directly inline inside the corresponding paragraph chunk as `[FIGURE_CAPTION: ...]`.

---

### 2. Format Processing Specifications

#### A. Markdown (`.md`) Files
*   Parsed using AST Markdown parsers (`mistletoe` or `markdown`).
*   Splits documents along logical header boundaries (`# H1`, `## H2`, `### H3`).
*   Code blocks (```python) are preserved intact within a single chunk.

#### B. PDF (`.pdf`) Documents
*   Parsed using **Azure AI Document Intelligence (Layout Model)**.
*   Extracts text while preserving multi-column reading order.
*   Tables are converted to HTML/Markdown tables (`<table>...</table>`) so column-row relationships are maintained during vector embedding.

#### C. Word (`.docx`) Documents
*   Parsed using `python-docx` or Document Intelligence layout.
*   Extracts heading styles (`Heading 1`, `Heading 2`) for logical boundaries.
*   Extracts tables as Markdown table strings.

---

## Section 3: Dynamic Chunking Matrix for .MD, .PDF, & .DOCX

| File Format | Primary Chunking Logic | Target Token Size | Overlap | Special Handling |
| :--- | :--- | :--- | :--- | :--- |
| **Markdown (`.md`)** | Semantic Header Splitting | 800 - 1,200 Tokens | 100 Tokens | Keeps code blocks and bullet lists whole within header sections. |
| **PDF (`.pdf`)** | Structural Layout Splitting | 512 - 1,024 Tokens | 128 Tokens | Injects GPT-4o Vision image captions inline; keeps tables whole. |
| **Word (`.docx`)** | Paragraph & Heading Splitting | 512 - 1,024 Tokens | 128 Tokens | Preserves table structures and document properties. |

---

## Section 4: Azure AI Search Vector Index Schema

```json
{
  "name": "doc-md-pdf-vector-index",
  "fields": [
    { "name": "chunk_id", "type": "Edm.String", "key": true, "searchable": false },
    { "name": "file_name", "type": "Edm.String", "searchable": true, "filterable": true },
    { "name": "file_type", "type": "Edm.String", "filterable": true, "facetable": true },
    { "name": "header_path", "type": "Edm.String", "searchable": true },
    { "name": "content", "type": "Edm.String", "searchable": true },
    { "name": "has_embedded_images", "type": "Edm.Boolean", "filterable": true },
    { 
      "name": "content_vector", 
      "type": "Collection(Edm.Single)", 
      "searchable": true, 
      "dimensions": 3072, 
      "vectorSearchProfile": "hnsw-profile" 
    }
  ],
  "vectorSearch": {
    "algorithms": [
      {
        "name": "hnsw-config",
        "kind": "hnsw",
        "hnswParameters": { "m": 4, "efConstruction": 400, "efSearch": 500, "metric": "cosine" }
      }
    ],
    "profiles": [
      { "name": "hnsw-profile", "algorithm": "hnsw-config" }
    ]
  },
  "semantic": {
    "configurations": [
      {
        "name": "semantic-config",
        "prioritizedFields": {
          "titleField": { "fieldName": "file_name" },
          "prioritizedContentFields": [{ "fieldName": "content" }]
        }
      }
    ]
  }
}
```

---

## Section 5: Agentic Multi-Query Retrieval Workflow

```
┌────────────────────────────────────────────────────────────────────────┐
│             Agentic Query Execution Loop for Docs & Code               │
├────────────────────────────────────────────────────────────────────────┤
│  1. User Query: "Compare PDF architecture diagram with MD spec"        │
│  2. LLM Decomposes into Sub-Queries:                                   │
│     - Query A (Filter file_type='pdf'): "Extract architecture diagram" │
│     - Query B (Filter file_type='md'): "Extract MD spec requirements"  │
│  3. Execute Parallel Hybrid Search (Vector HNSW + BM25 Keyword + RRF) │
│  4. Apply L2 Semantic Reranker (@search.rerankerScore)                 │
│  5. Synthesize Grounded Answer with Inline Citations                   │
└────────────────────────────────────────────────────────────────────────┘
```
