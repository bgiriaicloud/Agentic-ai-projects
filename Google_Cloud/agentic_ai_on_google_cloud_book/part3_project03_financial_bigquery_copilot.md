# Project 03: Enterprise Financial & Analytics BigQuery SQL Copilot

## 🎯 Executive Overview & Business Objective
A conversational enterprise SQL copilot that translates complex natural language financial inquiries into validated BigQuery SQL queries, executes queries with cost-budget guardrails, and renders interactive charts.

---

## 🏗️ System Architecture

```
[User Business Question: "Show top 5 revenue segments in Q3"]
        │
        ▼
[FastAPI Backend / Streamlit UI]
        │
        ▼
[Gemini 2.0 Flash: Text-to-SQL + Schema Understanding]
        │
        ▼ (Dry-Run Cost Calculation Guardrail)
[BigQuery Client: Query Execution (<100MB scan limit)]
        │
        ▼
[Table & Chart Visualizer + Looker Studio Embed]
```

---

## 💻 Production Implementation Code (BigQuery SQL Copilot)

```python
from google.cloud import bigquery
from vertexai.generative_models import GenerativeModel

bq_client = bigquery.Client()
sql_model = GenerativeModel("gemini-2.0-flash-exp")

def generate_and_run_safe_sql(natural_language_prompt: str, schema_ddl: str) -> dict:
    # 1. Generate SQL
    prompt = f"Schema:\n{schema_ddl}\n\nQuestion: {natural_language_prompt}\nGenerate valid Google Standard SQL."
    sql = sql_model.generate_content(prompt).text.strip().replace("```sql", "").replace("```", "")
    
    # 2. Dry Run for Cost Control
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=True)
    dry_run_job = bq_client.query(sql, job_config=job_config)
    
    bytes_scanned = dry_run_job.total_bytes_processed
    if bytes_scanned > 500 * 1024 * 1024: # 500MB safety ceiling
        return {"error": f"Query rejected: Exceeds 500MB cost ceiling (Scanned: {bytes_scanned} bytes)"}
    
    # 3. Execute Query
    results = [dict(row) for row in bq_client.query(sql).result(max_results=50)]
    return {"sql": sql, "bytes_processed": bytes_scanned, "data": results}
```
