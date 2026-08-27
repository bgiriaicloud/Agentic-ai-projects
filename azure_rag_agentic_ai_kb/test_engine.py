"""
Unit Test Suite for Azure Agentic Retrieval Engine
"""

import unittest
from agentic_retrieval_engine import AgenticRetrievalEngine, ReasoningEffort, SearchType


class TestAgenticRetrievalEngine(unittest.TestCase):
    def setUp(self):
        self.engine = AgenticRetrievalEngine(execution_mode="mock")

    def test_minimal_reasoning_effort(self):
        """Test that minimal reasoning effort skips LLM decomposition."""
        query = "Find beachfront hotels with airport shuttle and vegan restaurants"
        result = self.engine.execute_retrieval(query=query, reasoning_effort=ReasoningEffort.MINIMAL)
        
        self.assertEqual(result.reasoning_effort, ReasoningEffort.MINIMAL)
        self.assertEqual(len(result.subqueries), 1)
        self.assertEqual(result.subqueries[0].rationale, "Direct query dispatch without LLM decomposition.")
        self.assertTrue(len(result.retrieved_chunks) > 0)
        self.assertTrue(len(result.grounded_answer) > 0)

    def test_low_reasoning_effort_query_decomposition(self):
        """Test that low reasoning effort breaks multi-intent query into subqueries."""
        query = "Find me a hotel near the beach, with airport shuttle, and near vegetarian restaurants"
        result = self.engine.execute_retrieval(query=query, reasoning_effort=ReasoningEffort.LOW)
        
        self.assertEqual(result.reasoning_effort, ReasoningEffort.LOW)
        self.assertGreaterEqual(len(result.subqueries), 2)
        
        # Verify subqueries target different knowledge sources
        target_sources = {sq.target_source_id for sq in result.subqueries}
        self.assertIn("ks-hotels", target_sources)
        self.assertIn("ks-transport", target_sources)
        self.assertIn("ks-dining", target_sources)

    def test_semantic_reranker_sorting(self):
        """Test that retrieved chunks are correctly sorted by semantic reranking score."""
        query = "beachfront hotel with airport shuttle"
        result = self.engine.execute_retrieval(query=query, reasoning_effort=ReasoningEffort.LOW)
        
        scores = [chunk.semantic_rerank_score for chunk in result.retrieved_chunks]
        self.assertEqual(scores, sorted(scores, reverse=True), "Chunks must be ordered by descending semantic rerank score")

    def test_metrics_and_cost_calculation(self):
        """Test token estimation and pricing metrics calculation."""
        query = "find resort near beach"
        result = self.engine.execute_retrieval(query=query, reasoning_effort=ReasoningEffort.LOW)
        
        metrics = result.metrics
        self.assertIn("latency_ms", metrics)
        self.assertIn("estimated_cost_usd", metrics)
        self.assertIn("planner_input_tokens", metrics)
        self.assertGreater(metrics["estimated_cost_usd"], 0)


if __name__ == "__main__":
    unittest.main()
