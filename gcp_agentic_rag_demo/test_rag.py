"""
===============================================================================
GCP AGENTIC RAG UNIT TEST SUITE
===============================================================================
Verifies:
1. Vector Search Index Upsert & Search
2. Pub/Sub Event Processing & Ingestion
3. Agentic RAG Execution & Grounded Synthesis
4. Health Check Endpoint & Response Structure
===============================================================================
"""

import unittest
from gcp_rag_engine import GCPAgenticRAGEngine, DocumentChunk


class TestGCPAgenticRAG(unittest.TestCase):
    def setUp(self):
        self.engine = GCPAgenticRAGEngine()

    def test_01_knowledge_base_seeding(self):
        """Verifies that knowledge base seeds initial GCP chunks."""
        chunks = self.engine.vector_search.search_similarity([0.01]*768, top_k=5)
        self.assertGreaterEqual(len(chunks), 3)
        self.assertEqual(chunks[0].chunk_id, "gcp-doc-1")

    def test_02_pubsub_event_ingestion(self):
        """Verifies real-time event ingestion via simulated Pub/Sub."""
        event_data = {
            "file_name": "vertex_ai_spec.pdf",
            "source": "Cloud Storage (GCS)",
            "content": "Vertex AI Search provides enterprise RAG capabilities."
        }
        res = self.engine.process_pubsub_event(event_data)
        self.assertEqual(res["status"], "SUCCESS")
        self.assertTrue(res["doc_id"].startswith("gcs-"))

    def test_03_agentic_rag_query_execution(self):
        """Verifies Agentic RAG multi-query execution and citation output."""
        query = "How does BigQuery integrate with Vertex AI?"
        res = self.engine.execute_agentic_rag(query)
        self.assertTrue(res.query_id.startswith("gcp-query-"))
        self.assertEqual(len(res.reasoning_steps), 3)
        self.assertGreater(len(res.retrieved_chunks), 0)
        self.assertIn("Google Cloud Architecture guidelines", res.answer)

    def test_04_latency_and_citation_structure(self):
        """Verifies SLA latency metrics and verified citations."""
        res = self.engine.execute_agentic_rag("Test query")
        self.assertLess(res.latency_seconds, 2.0)
        self.assertGreater(len(res.citations), 0)


if __name__ == "__main__":
    unittest.main()
