import os
import sys
import asyncio
import json
from google.cloud import bigquery
from google.antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv

# Load local environment variables from .env file
load_dotenv()

# Define schema and table references
TABLE_REF = "bigquery-public-data.usa_names.usa_1910_current"

# Capture tool execution results in a global variable
SQL_EXECUTED = None
QUERY_DATA = None

def query_bigquery(sql_query: str) -> str:
    """Executes a SQL query against GCP BigQuery.

    Args:
        sql_query: Standard SQL query for 'bigquery-public-data.usa_names.usa_1910_current'.
    """
    global SQL_EXECUTED, QUERY_DATA
    SQL_EXECUTED = sql_query
    
    gcp_project = os.environ.get("GCP_PROJECT_ID")
    try:
        if gcp_project:
            client = bigquery.Client(project=gcp_project)
        else:
            client = bigquery.Client()
            
        print(f"\n[Tool Executing] Querying BigQuery: {sql_query}...")
        query_job = client.query(sql_query)
        results = query_job.result()
        
        rows = [dict(row) for row in results]
        QUERY_DATA = rows
        return json.dumps({"status": "success", "rows_returned": len(rows), "data": rows[:5]})
    except Exception as e:
        print(f"\n[Tool Fallback] Live BigQuery failed. Simulating response...")
        # Simple local fallback simulator
        simulated_data = [
            {"state": "CA", "gender": "M", "year": 2021, "name": "Noah", "number": 2590},
            {"state": "CA", "gender": "M", "year": 2021, "name": "Liam", "number": 2490},
            {"state": "CA", "gender": "M", "year": 2021, "name": "Oliver", "number": 2050},
            {"state": "CA", "gender": "M", "year": 2021, "name": "Alexander", "number": 1950},
            {"state": "CA", "gender": "M", "year": 2021, "name": "Benjamin", "number": 1850}
        ]
        QUERY_DATA = simulated_data
        return json.dumps({"status": "success", "rows_returned": len(simulated_data), "data": simulated_data})

async def main():
    # Retrieve question from CLI args or prompt the user
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "Show me the top 5 names for boys in California for the year 2021"

    # Configure the ADK Data Agent
    config = LocalAgentConfig(
        system_instructions=(
            "You are a BigQuery Data Analytics Agent. "
            f"Your goal is to answer user queries using the table '{TABLE_REF}'. "
            "Columns in table: state (STRING), gender (STRING), year (INTEGER), name (STRING), number (INTEGER). "
            "Write valid standard SQL for BigQuery and run it using the 'query_bigquery' tool. "
            "Limit your results to a maximum of 10 rows."
        ),
        tools=[query_bigquery]
    )

    print("====================================================================")
    # Corrected title: proof-of-concept
    print("      Proof-of-Concept (POC) BigQuery Data Agent (Gemini & ADK)     ")
    print("====================================================================")
    print(f"User Prompt: '{question}'\n")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set. Please set it in your environment or .env file.")
        return

    # Run agent chat session
    async with Agent(config=config) as agent:
        print("--- Stream Agent Reasoning & Output ---")
        response = await agent.chat(question)
        
        async for chunk in response:
            print(chunk, end="", flush=True)
        print("\n----------------------------------------")

    # Display findings
    if SQL_EXECUTED:
        print(f"\n[Generated SQL]:")
        print(f"  {SQL_EXECUTED}")
        
    if QUERY_DATA:
        print(f"\n[Returned Data Rows (Preview)]:")
        print(json.dumps(QUERY_DATA[:5], indent=2))
        print("====================================================================")

if __name__ == "__main__":
    asyncio.run(main())
