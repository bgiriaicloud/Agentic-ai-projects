# Azure Agentic Retrieval & RAG Reference Architecture

This directory contains the reference implementation, SDKs, web application engines, and architectural planning guides for building **Agentic RAG Platforms** on Microsoft Azure.

---

## 📖 Primary Guides & Projects

* 📄 [**`enterprise_agentic_rag_azure_plan.md`**](file:///Users/biswanathgiri/GenAI%26AgenticAI%20-Learing%20Roadmap/azure_rag_agentic_ai_kb/enterprise_agentic_rag_azure_plan.md): Comprehensive architecture guide and implementation plan covering:
  - **Multi-Source Ingestion**: SharePoint Online, Azure DevOps (Wikis, Boards, Repos), GitHub Repos.
  - **Multimodal Document Extraction**: Azure AI Document Intelligence layout parsing for PDFs/DOCX/PPTX, AST parsers for Markdown/Code, and GPT-4o Vision OCR for images/diagrams.
  - **Format-Aware Chunking Matrix**: Header-based Markdown chunking, slide-level PPTX chunking, AST code-aware chunking.
  - **Azure AI Search Hybrid Retrieval**: Keyword BM25 + Vector HNSW (`text-embedding-3-large`) with Reciprocal Rank Fusion (RRF) and L2 Semantic Reranker.
  - **Security Trimming**: Entra ID (Azure AD) ACL security trimming filtering queries by user & group SIDs.
  - **Agentic Orchestration Workflow**: 4-Step multi-query planning, parallel retrieval, and grounded synthesis with citations.

* 🐍 [**`agentic_retrieval_engine.py`**](file:///Users/biswanathgiri/GenAI%26AgenticAI%20-Learing%20Roadmap/azure_rag_agentic_ai_kb/agentic_retrieval_engine.py): Python SDK implementing the 4-step Azure AI Search Agentic Retrieval Engine.
* 🌐 [**`app.py`**](file:///Users/biswanathgiri/GenAI%26AgenticAI%20-Learing%20Roadmap/azure_rag_agentic_ai_kb/app.py): FastAPI web server running on port **8000** with an interactive glassmorphic web dashboard (`static/index.html`).
* 🧪 [**`test_engine.py`**](file:///Users/biswanathgiri/GenAI%26AgenticAI%20-Learing%20Roadmap/azure_rag_agentic_ai_kb/test_engine.py): Automated unit testing suite (`4/4 tests passed`).
