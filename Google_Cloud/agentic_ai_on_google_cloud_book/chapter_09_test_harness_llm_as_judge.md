# Chapter 9: Test Harness Engineering & Evaluation (LLM-as-a-Judge)

> *"You cannot deploy what you cannot measure. Test harnesses ensure your agents behave reliably, safely, and accurately under all edge cases."*

---

## 9.1 The 3 Pillars of Agent Evaluation

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AGENT EVALUATION METRICS                        │
├────────────────────────────────────────────────────────────────────────┤
│  1. Groundedness / Faithfulness: Is the output factual to retrieved doc?│
│  2. Answer Relevance           : Does the answer solve the user goal?  │
│  3. Tool Calling Accuracy      : Were correct functions called with args?│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 9.2 Building an Automated LLM-as-a-Judge Evaluator

```python
import json
from vertexai.generative_models import GenerativeModel

judge_model = GenerativeModel("gemini-2.0-pro-exp")

def evaluate_agent_response(query: str, retrieved_context: str, agent_answer: str) -> dict:
    """Uses Gemini 2.0 Pro as an automated Judge to grade agent groundedness and relevance."""
    prompt = f"""
    You are an impartial AI Quality Judge. Grade the agent's answer based on the retrieved context.
    
    User Query: {query}
    Retrieved Context: {retrieved_context}
    Agent Answer: {agent_answer}
    
    Output JSON format with:
    - groundedness_score (1 to 5)
    - relevance_score (1 to 5)
    - explanation (short string)
    """
    response = judge_model.generate_content(prompt)
    return json.loads(response.text.strip().replace("```json", "").replace("```", ""))
```

---

## 9.3 Mock Sandboxing & CI/CD Integration

To test agents safely in **Cloud Build** before production deployment:
1. **Mock External APIs**: Mock BigQuery and Cloud Storage calls using `unittest.mock`.
2. **Golden Test Suites**: Run 50+ benchmark test cases measuring average accuracy and regression scores.
3. **Threshold Assertion**: Fail the CI/CD build if average Groundedness drops below $4.5/5.0$.

---

## 9.4 Chapter Summary & Key Takeaways

* **LLM-as-a-Judge** provides scalable, automated scoring of complex natural language responses.
* **Hermetic Sandboxing** in CI/CD ensures agents are regression-tested before merge.
* **Next Chapter**: In [Chapter 10](chapter_10_production_mlops_security.md), we deploy agent systems to production on **Cloud Run** and **GKE**.
