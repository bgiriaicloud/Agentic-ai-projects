# FinOps for the Agentic Harness: Simulator & Cost Analyzer

This interactive tool models, simulates, and calculates the unit economics and hidden costs of non-functional LLM calls in enterprise Agentic Harnesses.

---

## The Non-Functional Token Multiplier

In production agent harnesses, for every 1 user turn, the harness executes auxiliary background calls for:
1. **Pre-Execution Guardrails**: Prompt injection, jailbreak scanning, PII redaction.
2. **Memory & Context**: Working memory summarization, episodic memory extraction, listwise candidate reranking.
3. **Post-Execution Guardrails**: Full context groundedness & hallucination audits, egress PII redaction.
4. **Automated Evals (LLM-as-a-Judge)**: Context relevance, trajectory fidelity, safety scoring.

In an unmanaged harness, these non-functional calls account for **75% to 85% of total LLM token spend**, driving a **Token Amplification Factor (TAF) of 8× to 15×**.

---

## FinOps Optimization Techniques Demonstrated

1. **Model Cascading & SLM Offloading**: Offloading safety, guardrails, and summarization to specialized Small Language Models (e.g., Llama-Guard 3 8B, Gemini 1.5 Flash) at 95%+ lower cost.
2. **Deterministic Heuristic 1st**: Using regex and Aho-Corasick filters to eliminate 0-token overhead on obvious attacks and PII.
3. **Prompt Prefix Caching**: Structuring static system personas and tool definitions to benefit from 50%–90% provider prompt caching discounts.
4. **Asynchronous Sampled Evals**: Replacing 100% inline synchronous LLM-as-a-judge calls with a 5% stratified random sample processed via off-peak Batch APIs (50% discount).
5. **Adaptive Post-Guardrails**: Skipping expensive groundedness re-verification when deterministic tool proofs provide high confidence.

---

## How to Run the Simulator

From the repository root:

```bash
python3 -m finops_agentic_harness.run_simulation
```

Or execute directly:

```bash
python3 finops_agentic_harness/run_simulation.py
```

### Outputs
- **Console Breakdown**: Full span-by-span token and USD cost breakdown for both Unmanaged and FinOps-Governed scenarios.
- **Unit Economics**: Token Amplification Factor (TAF), Non-Functional Token Ratio (NFTR), Non-Functional Cost Ratio (NFCR).
- **Executive Monthly Summary**: Projected savings across 4,000,000 monthly turns.
- **Exported Telemetry**: Detailed JSON output saved to `finops_agentic_harness/finops_simulation_report.json`.
