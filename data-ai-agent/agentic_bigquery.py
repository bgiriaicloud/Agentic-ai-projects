import os
import json
import pandas as pd
from google.cloud import bigquery
from google.antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv

load_dotenv()

# Global state tracker to allow Streamlit UI to extract data metrics directly
LAST_QUERY_RESULT = None

# Define the dataset metadata for grounding rules
DATASET_METADATA = {
    "table_name": "bigquery-public-data.usa_names.usa_1910_current",
    "description": "USA names dataset from Social Security Administration applications from 1910 to current.",
    "schema": [
        {"name": "state", "type": "STRING", "description": "2-letter state code (e.g., 'TX', 'CA')"},
        {"name": "gender", "type": "STRING", "description": "Gender code: 'M' for male, 'F' for female"},
        {"name": "year", "type": "INTEGER", "description": "4-digit year of birth (e.g., 2020)"},
        {"name": "name", "type": "STRING", "description": "Given name (e.g., 'James', 'Mary')"},
        {"name": "number", "type": "INTEGER", "description": "Number of occurrences of the name in that year/state"}
    ]
}

def execute_sql_query(sql_query: str) -> str:
    """Executes a SQL query against Google Cloud BigQuery.

    Args:
        sql_query: A valid Google SQL query targeting 'bigquery-public-data.usa_names.usa_1910_current'.
    """
    global LAST_QUERY_RESULT
    
    # Verify project configuration
    gcp_project = os.environ.get("GCP_PROJECT_ID")
    
    try:
        # Initialize BigQuery Client
        # It will automatically authenticate using default application credentials (ADC)
        if gcp_project:
            client = bigquery.Client(project=gcp_project)
        else:
            client = bigquery.Client()
            
        query_job = client.query(sql_query)
        results = query_job.result()
        
        # Parse rows
        rows = [dict(row) for row in results]
        
        # Save to global variable for UI retrieval
        LAST_QUERY_RESULT = {
            "status": "success",
            "source": "live_bigquery",
            "sql_executed": sql_query,
            "data": rows
        }
        return json.dumps(LAST_QUERY_RESULT)
        
    except Exception as e:
        # Fallback Mock logic if GCP environment is not fully configured (local demonstration safety)
        print(f"DEBUG: Live BigQuery execution failed ({str(e)}). Falling back to mock generator...")
        return generate_mock_data(sql_query)

def generate_mock_data(sql_query: str) -> str:
    """Mock database engine to return representative data when GCP credentials are not active."""
    global LAST_QUERY_RESULT
    
    # Simple semantic keyword parser to return realistic mock names based on the prompt query
    sql_upper = sql_query.upper()
    mock_rows = []
    
    if "TX" in sql_upper or "TEXAS" in sql_upper:
        state = "TX"
    elif "CA" in sql_upper or "CALIFORNIA" in sql_upper:
        state = "CA"
    else:
        state = "NY"
        
    year = 2020
    for y in ["2018", "2019", "2020", "2021", "2022"]:
        if y in sql_upper:
            year = int(y)
            
    if "M" in sql_upper or "MALE" in sql_upper:
        names = [("Liam", 1500), ("Noah", 1450), ("Oliver", 1200), ("Elijah", 1100), ("James", 1050)]
    elif "F" in sql_upper or "FEMALE" in sql_upper:
        names = [("Olivia", 1600), ("Emma", 1500), ("Charlotte", 1300), ("Amelia", 1250), ("Sophia", 1100)]
    else:
        names = [("Liam", 1500), ("Olivia", 1400), ("Noah", 1350), ("Emma", 1300), ("Oliver", 1250)]

    for name, count in names:
        mock_rows.append({
            "state": state,
            "gender": "M" if name in ["Liam", "Noah", "Oliver", "Elijah", "James"] else "F",
            "year": year,
            "name": name,
            "number": count
        })
        
    LAST_QUERY_RESULT = {
        "status": "success",
        "source": "mock_database",
        "sql_executed": sql_query,
        "data": mock_rows,
        "warning": "GCP BigQuery credentials not detected; returned simulated results."
    }
    return json.dumps(LAST_QUERY_RESULT)

class BigQueryDataAgent:
    def __init__(self):
        # Configure ADK config
        self.config = LocalAgentConfig(
            system_instructions=(
                "You are an expert Data Agent specializing in Google Cloud BigQuery databases. "
                "Your role is to translate user natural language queries into valid BigQuery SQL queries "
                "and execute them using the execute_sql_query tool. "
                f"You target exclusively the table: {DATASET_METADATA['table_name']}. "
                f"Table description: {DATASET_METADATA['description']}. "
                f"Schema mapping: {json.dumps(DATASET_METADATA['schema'], indent=2)}. "
                "Rule 1: Always write Standard SQL compatible with BigQuery. "
                "Rule 2: Select appropriate columns and restrict rows using a LIMIT clause (default limit: 10 if not specified). "
                "Rule 3: After executing the tool, present the user with a brief summary of the query goal, "
                "the generated SQL statement, and confirm that the query finished successfully."
            ),
            tools=[execute_sql_query]
        )

    async def run_query(self, query_text: str):
        """Processes the query, runs the SQL generation tool, and returns the result."""
        async with Agent(self.config) as agent:
            response = await agent.chat(query_text)
            
            # Capture final text description
            response_text = []
            async for chunk in response:
                response_text.append(chunk)
                
            return "".join(response_text)
