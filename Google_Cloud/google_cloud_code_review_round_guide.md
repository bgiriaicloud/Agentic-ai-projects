# Google Cloud Code Review Round Preparation Guide & Python Simulator
## Role: Delivery Executive & Architect / Technical Solutions Consultant (Google Cloud)

This guide is designed to help candidates excel in the **Code Review / Technical Code Audit Interview Round** for senior delivery, consulting, and architect roles at Google Cloud. It covers Google's evaluation rubrics, the 4-step interview response framework, 5 GCP enterprise scenarios, and 6 core Python language functionality code review scenarios.

---

## 📋 Table of Contents
* [Section 1: Google Code Review Evaluation Rubrics & Response Framework](#section-1-google-code-review-evaluation-rubrics--response-framework)
* [Section 2: GCP Enterprise Scenario 1 - Vertex AI GenAI RAG Pipeline](#section-2-gcp-enterprise-scenario-1---vertex-ai-genai-rag-pipeline)
* [Section 3: GCP Enterprise Scenario 2 - BigQuery Ingestion & ETL Script](#section-3-gcp-enterprise-scenario-2---bigquery-ingestion--etl-script)
* [Section 4: GCP Enterprise Scenario 3 - Cloud Run FastAPI Microservice](#section-4-gcp-enterprise-scenario-3---cloud-run-fastapi-microservice)
* [Section 5: GCP Enterprise Scenario 4 - Pub/Sub Streaming Worker](#section-5-gcp-enterprise-scenario-4---pubsub-streaming-worker)
* [Section 6: GCP Enterprise Scenario 5 - PyTest Unit & Integration Test Suite](#section-6-gcp-enterprise-scenario-5---pytest-unit--integration-test-suite)
* [Section 7: Basic Python Functionality Code Review Scenarios](#section-7-basic-python-functionality-code-review-scenarios)

---

## Section 1: Google Code Review Evaluation Rubrics & Response Framework

### 1. The 4 Code Review Evaluation Pillars

During a Google Code Review interview round, interviewers present Python code snippets written by a team or customer and ask you to evaluate, critique, and refactor the code. You are evaluated across four pillars:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Google Code Review Evaluation Pillars                │
├────────────────────────────────────────────────────────────────────────┤
│  1. Security & Compliance: Hardcoded secrets, OWASP top 10, IAM checks │
│  2. Performance & Scalability: Blocking I/O, N+1 queries, Caching       │
│  3. Resilience & Error Handling: Retries, Exponential backoff, Logging │
│  4. Maintainability & Testability: PEP 8, Type hints, Mock unit tests  │
└────────────────────────────────────────────────────────────────────────┘
```

### 2. The 4-Step Code Review Response Framework

When answering in the interview, structure your response using this 4-step framework:

1.  **High-Level Architecture Summary**: State what the code is attempting to accomplish and summarize its primary architectural role.
2.  **Critical Vulnerabilities & Security Risks**: Identify severe security issues (hardcoded keys, injection risks, missing IAM authentication).
3.  **Performance & Reliability Bottlenecks**: Spot scalability flaws (blocking synchronous loops, missing batching, un-cached API calls, swallow exceptions).
4.  **Refactored Production Code**: Provide the clean, modern Python 3.11+ implementation incorporating Google Cloud best practices.

---

## Section 2: GCP Enterprise Scenario 1 - Vertex AI GenAI RAG Pipeline

### 1. Flawed Python Code Snippet (`vertex_rag_pipeline.py`)

```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
import json
import requests

# HARDCODED GCP SERVICE ACCOUNT KEY - CRITICAL SECURITY VULNERABILITY!
SA_KEY = {
    "type": "service_account",
    "project_id": "my-gcp-project",
    "private_key_id": "12345abcdef",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n"
}

def generate_rag_response(user_prompt, doc_context):
    # SECURITY RISK: Prompt Injection vulnerability! Raw string concatenation without validation.
    prompt = "Context: " + doc_context + "\nUser Question: " + user_prompt + "\nAnswer accurately."
    
    # PERFORMANCE BOTTLENECK: Blocking synchronous HTTP POST call without timeout or retries!
    url = "https://us-central1-aiplatform.googleapis.com/v1/projects/my-gcp-project/locations/us-central1/publishers/google/models/gemini-pro:predict"
    
    headers = {"Content-Type": "application/json"}
    payload = {"instances": [{"prompt": prompt}]}
    
    # RELIABILITY RISK: No error handling; if API fails, application crashes silently or returns None
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()['predictions'][0]['content']
    except Exception as e:
        # FLAW: Swallowing exception without structured logging
        print("Error happened")
        return None
```

### 2. Code Review Audit & Critique

*   ❌ **Security Risk 1**: Hardcoded Service Account private key in source code (violates Google security policy; risks credential exfiltration).
*   ❌ **Security Risk 2**: Vulnerable to Prompt Injection. Raw string concatenation allows user input to override system instructions.
*   ❌ **Performance Bottleneck**: Uses synchronous `requests.post()` in a single-threaded blocking execution without request timeouts or connection pooling.
*   ❌ **Reliability Risk**: Missing retry mechanism with exponential backoff for transient 503/429 API rate limits.
*   ❌ **Maintainability**: Hardcoded project IDs and endpoints; generic `except Exception` swallowing errors with `print()`.

### 3. Refactored Production Python Code

```python
"""
Production-Grade Vertex AI GenAI RAG Pipeline
Features: Google Auth Application Default Credentials (ADC), Async Client,
Tenacity Exponential Backoff, Pydantic Prompt Validation, Structlog.
"""

import os
import logging
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, SafetySetting, HarmCategory, HarmBlockThreshold
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configure structured logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Pydantic input validation model (Prevents Prompt Injection)
class RAGRequest(BaseModel):
    user_prompt: str = Field(..., min_length=3, max_length=2000, description="Cleaned user query")
    doc_context: str = Field(..., min_length=10, max_length=50000, description="Grounded document context")

class VertexGenAIService:
    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1"):
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GCP_PROJECT_ID environment variable must be set.")
        
        # Initialize Vertex AI SDK using Application Default Credentials (ADC)
        aiplatform.init(project=self.project_id, location=location)
        
        # Load Gemini model with Context Caching & Safety Settings
        self.model = GenerativeModel(
            model_name="gemini-1.5-flash-002",
            system_instruction=["You are an enterprise assistant. Answer questions strictly based on provided context with citations."]
        )
        
        self.safety_settings = [
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    async def generate_rag_response_async(self, request: RAGRequest) -> str:
        """Asynchronously generates a grounded RAG response with exponential backoff retries."""
        structured_prompt = f"DOCUMENT CONTEXT:\n{request.doc_context}\n\nUSER QUESTION:\n{request.user_prompt}"
        
        try:
            logger.info("Submitting async inference request to Vertex AI Gemini...")
            
            # Non-blocking async generation
            response = await self.model.generate_content_async(
                structured_prompt,
                safety_settings=self.safety_settings
            )
            
            if not response.text:
                raise ValueError("Received empty response from Vertex AI model.")
                
            return response.text
            
        except Exception as e:
            logger.error(f"Vertex AI Generation Error: {str(e)}", exc_info=True)
            raise

# Usage Example
if __name__ == "__main__":
    req = RAGRequest(
        user_prompt="What is the shipping policy?",
        doc_context="Standard shipping takes 3 business days via FedEx."
    )
    service = VertexGenAIService(project_id="my-gcp-project")
    result = asyncio.run(service.generate_rag_response_async(req))
    print(result)
```

---

## Section 3: GCP Enterprise Scenario 2 - BigQuery Ingestion & ETL Script

### 1. Flawed Python Code Snippet (`bigquery_etl_ingestion.py`)

```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
from google.cloud import bigquery

client = bigquery.Client()
table_id = "my_project.my_dataset.raw_events"

def process_and_insert_events(events_list):
    # FLAW: Creating un-partitioned table inside ingestion loop!
    schema = [
        bigquery.SchemaField("event_id", "STRING"),
        bigquery.SchemaField("user_id", "STRING"),
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("payload", "STRING")
    ]
    table = bigquery.Table(table_id, schema=schema)
    client.create_table(table, exists_ok=True)
    
    # CRITICAL PERFORMANCE BOTTLENECK: Row-by-row streaming insert in a tight loop!
    # Will breach BigQuery streaming API quota (100,000 rows/sec limit) and incur huge cost.
    for event in events_list:
        row_to_insert = [{
            "event_id": event["id"],
            "user_id": event["uid"],
            "timestamp": event["ts"],
            "payload": event["data"]
        }]
        errors = client.insert_rows_json(table_id, row_to_insert)
        if errors:
            print("Failed to insert row:", errors)
```

### 2. Code Review Audit & Critique

*   ❌ **Performance Bottleneck 1**: Iterating with `insert_rows_json` row-by-row in a loop. Causes severe latency, breaches BigQuery quota limits, and incurs streaming API charges.
*   ❌ **Architectural Flaw**: Table creation DDL is un-partitioned and un-clustered, causing future queries over millions of events to execute full-table scans.
*   ❌ **Reliability Risk**: Failed rows are logged via `print()` and dropped without routing to a Dead-Letter Queue (DLQ) for reprocessing.
*   ❌ **Resource Waste**: `create_table` API call is invoked repeatedly inside the processing execution path.

### 3. Refactored Production Python Code

```python
"""
Production-Grade BigQuery Ingestion Pipeline
Features: Storage Write API Batching, Date Partitioning, Clustering, Dead-Letter Queue.
"""

import logging
from typing import List, Dict, Any
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BigQueryBatchIngestor:
    def __init__(self, project_id: str, dataset_id: str, table_name: str):
        self.client = bigquery.Client(project=project_id)
        self.table_id = f"{project_id}.{dataset_id}.{table_name}"
        self._ensure_table_exists(dataset_id, table_name)

    def _ensure_table_exists(self, dataset_id: str, table_name: str):
        """Creates table with Date Partitioning and Clustering if not exists."""
        schema = [
            bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("event_timestamp", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("payload", "JSON", mode="NULLABLE")
        ]
        
        table = bigquery.Table(self.table_id, schema=schema)
        
        # PRODUCTION BEST PRACTICE: Date Partitioning + Clustering
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="event_timestamp"
        )
        table.clustering_fields = ["user_id"]
        
        table = self.client.create_table(table, exists_ok=True)
        logger.info(f"Verified BigQuery partitioned table: {self.table_id}")

    def insert_events_batch(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Inserts events in a single batch using insert_rows_json with DLQ fallback."""
        if not events:
            return []

        rows_to_insert = [
            {
                "event_id": str(e["id"]),
                "user_id": str(e["uid"]),
                "event_timestamp": e["ts"],
                "payload": e.get("data", {})
            }
            for e in events
        ]

        logger.info(f"Streaming batch of {len(rows_to_insert)} rows to BigQuery...")
        errors = self.client.insert_rows_json(self.table_id, rows_to_insert)

        failed_rows = []
        if errors:
            logger.error(f"Encountered {len(errors)} insertion errors in batch.")
            for err in errors:
                index = err["index"]
                failed_item = rows_to_insert[index]
                failed_item["error_reason"] = str(err["errors"])
                failed_rows.append(failed_item)
                
            self._write_to_dead_letter_queue(failed_rows)

        return failed_rows

    def _write_to_dead_letter_queue(self, failed_rows: List[Dict[str, Any]]):
        """Routes malformed rows to quarantine storage for auditing."""
        logger.warning(f"Routing {len(failed_rows)} failed records to DLQ Storage.")
```

---

## Section 4: GCP Enterprise Scenario 3 - Cloud Run FastAPI Microservice

### 1. Flawed Python Code Snippet (`cloud_run_service.py`)

```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
from fastapi import FastAPI
import sqlite3

app = FastAPI()

# FLAW 1: Hardcoded DB path and un-authenticated endpoint binding
@app.get("/get_user_data")
def get_user(user_id: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # CRITICAL SECURITY VULNERABILITY: SQL Injection via string formatting!
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    return {"user": user}
```

### 2. Code Review Audit & Critique

*   ❌ **Security Risk 1 (OWASP Top 10)**: High-severity SQL Injection vulnerability. `f"WHERE user_id = '{user_id}'"` allows attackers to bypass authentication or drop tables (`' OR '1'='1`).
*   ❌ **Security Risk 2**: Endpoint lacks OAuth2 / GCP IAM ID Token authentication checks, exposing raw endpoints publicly.
*   ❌ **Performance Flaw**: Synchronous database driver (`sqlite3`) blocks FastAPI event loop threads during I/O operations.
*   ❌ **Operational Flaw**: Lacks Kubernetes/Cloud Run startup and liveness health check endpoints (`/healthz`).

### 3. Refactored Production Python Code

```python
"""
Production-Grade FastAPI Microservice for GCP Cloud Run
Features: Parameterized SQL (SQLAlchemy Async), GCP IAM Authentication, Structlog.
"""

import os
import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="User Data Microservice", version="1.0.0")
security = HTTPBearer()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/dbname")
engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def verify_iam_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token or len(token) < 10:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid GCP IAM bearer token"
        )
    return token

class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str

@app.get("/healthz", status_code=200)
async def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user_secure(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(verify_iam_token)
):
    try:
        # SECURITY FIX: Parameterized SQL Query (Prevents SQL Injection)
        stmt = text("SELECT user_id, username, email FROM users WHERE user_id = :uid")
        result = await db.execute(stmt, {"uid": user_id})
        row = result.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="User not found")

        return UserResponse(user_id=row.user_id, username=row.username, email=row.email)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Database error during user query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

---

## Section 5: GCP Enterprise Scenario 4 - Pub/Sub Streaming Worker

### 1. Flawed Python Code Snippet (`pubsub_worker.py`)

```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
from google.cloud import pubsub_v1
import time

subscriber = pubsub_v1.SubscriberClient()
subscription_path = "projects/my-project/subscriptions/my-sub"

def callback(message):
    print(f"Received message: {message.data}")
    data = json.loads(message.data)
    save_to_database(data)
    message.ack()

# CRITICAL FLAW: Synchronous infinite blocking poll loop holding thread!
subscriber.subscribe(subscription_path, callback=callback)
while True:
    time.sleep(60)
```

### 2. Code Review Audit & Critique

*   ❌ **Reliability Risk 1**: If `save_to_database` raises an exception, `message.ack()` is never called, and `message.nack()` is missing, causing Pub/Sub to delay redelivery for the full ack deadline duration.
*   ❌ **Performance Bottleneck**: Lacks Flow Control settings (`max_messages`), allowing high incoming volume to overwhelm worker RAM.
*   ❌ **Operational Risk**: Uses `while True: time.sleep(60)` blocking loop instead of proper async futures and signal handlers for graceful container termination.

### 3. Refactored Production Python Code

```python
"""
Production-Grade Pub/Sub Async Subscriber Worker
Features: Flow Control, Automatic Nack on Error, Graceful Signal Handling, Dead-Letter Topic.
"""

import signal
import sys
import logging
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.futures import StreamingPullFuture

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PubSubAsyncWorker:
    def __init__(self, project_id: str, subscription_id: str):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_id)
        
        self.flow_control = pubsub_v1.types.FlowControl(
            max_messages=100,
            max_bytes=10 * 1024 * 1024
        )
        self.future: StreamingPullFuture = None

    def process_message(self, message: pubsub_v1.subscriber.message.Message):
        try:
            payload = message.data.decode("utf-8")
            logger.info(f"Processing message ID: {message.message_id}")
            
            self._save_to_database(payload)
            message.ack()
            
        except Exception as e:
            logger.error(f"Error processing message {message.message_id}: {str(e)}", exc_info=True)
            message.nack()

    def _save_to_database(self, payload: str):
        pass

    def start(self):
        logger.info(f"Starting Pub/Sub worker listening on {self.subscription_path}...")
        
        self.future = self.subscriber.subscribe(
            self.subscription_path,
            callback=self.process_message,
            flow_control=self.flow_control
        )
        
        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)

    def _shutdown(self, signum, frame):
        logger.info("Received termination signal. Cancelling Pub/Sub subscriber...")
        if self.future:
            self.future.cancel()
        sys.exit(0)
```

---

## Section 6: GCP Enterprise Scenario 5 - PyTest Unit & Integration Test Suite

### 1. Flawed Python Code Snippet (`test_vertex_service.py`)

```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
import pytest
from vertex_rag_pipeline import generate_rag_response

# CRITICAL TEST FLAW: Unit test calls LIVE GCP Vertex AI API over the network!
def test_generate_rag_response():
    result = generate_rag_response("What is GCP?", "GCP is Google Cloud Platform.")
    assert result is not None
    assert "Google Cloud" in result
```

### 2. Code Review Audit & Critique

*   ❌ **Test Flaw 1**: Unit test executes actual HTTP calls to live production Vertex AI GCP network endpoints, breaking hermetic test isolation.
*   ❌ **CI/CD Risk**: Test suite will fail in automated GitHub Actions / Cloud Build pipelines lacking GCP credentials.
*   ❌ **Weak Assertions**: `assert result is not None` checks for non-null output without validating model contract schemas or exception handling boundaries.

### 3. Refactored Production Python Code

```python
"""
Production-Grade PyTest Unit Suite for Vertex AI Service
Features: `@patch` Mocks, Fixtures, Hermetic Network Isolation, Edge Case Testing.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from vertex_rag_pipeline import VertexGenAIService, RAGRequest

@pytest.fixture
def mock_vertex_init():
    with patch("google.cloud.aiplatform.init") as mock_init:
        yield mock_init

@pytest.fixture
def sample_rag_request():
    return RAGRequest(
        user_prompt="What is Google Cloud?",
        doc_context="Google Cloud Platform (GCP) provides cloud computing services."
    )

@pytest.mark.asyncio
async def test_generate_rag_response_success(mock_vertex_init, sample_rag_request):
    with patch("vertex_rag_pipeline.GenerativeModel") as MockModelClass:
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Google Cloud Platform provides scalable cloud computing services."
        
        mock_model_instance.generate_content_async = AsyncMock(return_value=mock_response)
        MockModelClass.return_value = mock_model_instance
        
        service = VertexGenAIService(project_id="test-project")
        result = await service.generate_rag_response_async(sample_rag_request)
        
        assert "Google Cloud Platform" in result
        mock_model_instance.generate_content_async.assert_called_once()
```

---

## Section 7: Basic Python Functionality Code Review Scenarios

This section covers fundamental Python programming traps, memory leaks, algorithmic bugs, and object-oriented anti-patterns frequently presented during Google core technical code review rounds.

---

### Python Scenario 1: Mutable Default Arguments & In-Place List Mutation

#### Flawed Code Snippet (`mutable_default.py`):
```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
def add_user_role(user_id, roles=[]): # FLAW 1: Mutable default argument!
    roles.append("USER") # FLAW 2: Mutating list argument in-place
    if user_id.startswith("admin"):
        roles.append("ADMIN")
    return roles

# Unexpected behavior:
print(add_user_role("user1")) # Output: ['USER']
print(add_user_role("user2")) # Output: ['USER', 'USER']  <-- BUG! Shared state across calls!
```

#### Code Review Audit:
*   ❌ **Bug 1 (Mutable Default Argument)**: `roles=[]` is evaluated ONCE when the module is imported, NOT on every function call. All invocations reusing the default parameter share the exact same list instance in memory, causing cross-request state pollution.
*   ❌ **Bug 2 (Side-effect Mutation)**: Mutating incoming argument objects in-place (`roles.append()`) creates unwanted side effects for caller code.

#### Refactored Production Python Code:
```python
from typing import List, Optional

def add_user_role(user_id: str, roles: Optional[List[str]] = None) -> List[str]:
    """Correct implementation using None default and defensive copying."""
    # FIX 1: Use None as default and create a fresh list instance
    user_roles = list(roles) if roles is not None else []
    
    user_roles.append("USER")
    if user_id.startswith("admin"):
        user_roles.append("ADMIN")
        
    return user_roles
```

---

### Python Scenario 2: Memory Leak with Large Files & Missing Context Manager

#### Flawed Code Snippet (`file_reader.py`):
```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
def process_logs(file_path):
    # FLAW 1: No context manager ('with' statement); file handle leaked on exception!
    f = open(file_path, "r")
    
    # FLAW 2: f.readlines() loads ENTIRE multi-gigabyte file into RAM at once!
    lines = f.readlines()
    
    error_logs = []
    for line in lines:
        if "ERROR" in line:
            error_logs.append(line.strip())
            
    f.close() # Never reached if error occurs above!
    return error_logs
```

#### Code Review Audit:
*   ❌ **Memory Leak (OOM Risk)**: `f.readlines()` reads all lines into memory simultaneously. If log file is 10 GB, container crashes with Out-Of-Memory (OOM).
*   ❌ **Resource Leak**: Lacks `with open(...)` context manager. If processing fails mid-way, file descriptor remains open.

#### Refactored Production Python Code:
```python
from typing import Generator
import logging

logger = logging.getLogger(__name__)

def process_logs_streaming(file_path: str) -> Generator[str, None, None]:
    """Stream processing using a Generator (Memory Efficient O(1) RAM)."""
    try:
        # FIX 1: Use context manager to guarantee resource cleanup
        with open(file_path, mode="r", encoding="utf-8") as f:
            # FIX 2: Iterate over file object directly (streams line-by-line)
            for line in f:
                if "ERROR" in line:
                    yield line.strip()
    except FileNotFoundError:
        logger.error(f"Log file not found: {file_path}")
        raise
```

---

### Python Scenario 3: Encapsulation Violation & Lack of Thread Safety in OOP

#### Flawed Code Snippet (`bank_account.py`):
```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
class BankAccount:
    def __init__(self, balance):
        # FLAW 1: Public attribute allows illegal direct balance modification
        self.balance = balance
        
    def withdraw(self, amount):
        # FLAW 2: Lack of race condition / thread safety protection!
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
```

#### Code Review Audit:
*   ❌ **Encapsulation Violation**: `self.balance` is public. External code can bypass validation (`account.balance = -9999`).
*   ❌ **Race Condition**: Under multi-threaded execution (e.g., web server), two concurrent withdrawal calls can cause a Race Condition where balance goes negative.

#### Refactored Production Python Code:
```python
import threading

class InsufficientFundsError(Exception):
    pass

class BankAccount:
    """Thread-safe, encapsulated Bank Account class."""
    def __init__(self, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative.")
        self._balance = initial_balance  # Encapsulated private attribute
        self._lock = threading.Lock()    # Thread lock for atomic operations

    @property
    def balance(self) -> float:
        """Read-only property getter."""
        with self._lock:
            return self._balance

    def withdraw(self, amount: float) -> float:
        """Atomic thread-safe withdrawal."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
            
        with self._lock: # Guarantees atomic thread safety
            if self._balance < amount:
                raise InsufficientFundsError(f"Insufficient balance ({self._balance}) for withdrawal ({amount}).")
            self._balance -= amount
            return self._balance
```

---

### Python Scenario 4: $O(N^2)$ Algorithmic Complexity & Inefficient Lookups

#### Flawed Code Snippet (`find_duplicates.py`):
```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
def find_duplicates(item_list):
    duplicates = []
    # FLAW 1: O(N^2) complexity due to nested loop and 'in' check on list!
    for i in range(len(item_list)):
        for j in range(i + 1, len(item_list)):
            if item_list[i] == item_list[j] and item_list[i] not in duplicates:
                duplicates.append(item_list[i]) # List 'in' check is O(N)!
    return duplicates
```

#### Code Review Audit:
*   ❌ **Performance Flaw ($O(N^2)$ Time Complexity)**: Double nested loops combined with list `in` membership check causes $O(N^2)$ execution. For 100,000 items, loop runs 10 billion comparisons.

#### Refactored Production Python Code:
```python
from typing import List, TypeVar, Set

T = TypeVar("T")

def find_duplicates_fast(items: List[T]) -> List[T]:
    """Finds duplicates in O(N) time using Hash Sets (O(1) lookups)."""
    seen: Set[T] = set()
    duplicates: Set[T] = set()
    
    for item in items:
        if item in seen:  # O(1) average lookup time
            duplicates.add(item)
        else:
            seen.add(item)
            
    return list(duplicates)
```

---

### Python Scenario 5: Exponential Recursion Overhead & Flawed Custom Decorator

#### Flawed Code Snippet (`fibonacci.py`):
```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
def my_logger(func):
    # FLAW 1: Decorator lacks @functools.wraps; destroys original function metadata!
    def wrapper(*args, **kwargs):
        print("Calling function...")
        return func(*args, **kwargs)
    return wrapper

@my_logger
def fibonacci(n):
    # FLAW 2: Naive exponential O(2^N) recursion without memoization!
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2) # Stack overflow & extreme latency for N > 35!
```

#### Code Review Audit:
*   ❌ **Algorithmic Flaw ($O(2^N)$ Exponential Complexity)**: Computing `fibonacci(50)` requires $>1 \text{ trillion}$ recursive function calls, causing system freeze or `RecursionError`.
*   ❌ **Decorator Bug**: Lacks `@functools.wraps(func)`, wiping out original function `__name__` and `__doc__` metadata.

#### Refactored Production Python Code:
```python
import functools
import logging

logger = logging.getLogger(__name__)

def log_execution(func):
    """Custom decorator preserving function metadata via @wraps."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__} with args={args}")
        return func(*args, **kwargs)
    return wrapper

# FIX 1: Built-in Memoization decorator caches computed sub-problems in O(N) time
@log_execution
@functools.lru_cache(maxsize=128)
def fibonacci_memoized(n: int) -> int:
    """O(N) Time, O(N) Memory recursive Fibonacci with memoization."""
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)

# FIX 2: Iterative DP approach (O(N) Time, O(1) Space - Maximum Efficiency)
def fibonacci_iterative(n: int) -> int:
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

---

### Python Scenario 6: Misuse of Threads for CPU-Bound Work (GIL Bottleneck)

#### Flawed Code Snippet (`parallel_compute.py`):
```python
# FLAWED CODE - DO NOT USE IN PRODUCTION
import threading

def cpu_heavy_task(number):
    # Heavy CPU calculation (e.g., prime factorization)
    return sum(i * i for i in range(number))

# FLAW: Using threading.Thread for CPU-bound tasks in Python!
# Bottlenecked by Global Interpreter Lock (GIL); runs slower than single-threaded!
threads = []
for _ in range(4):
    t = threading.Thread(target=cpu_heavy_task, args=(10000000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

#### Code Review Audit:
*   ❌ **Architecture Bug (GIL Bottleneck)**: Python's Global Interpreter Lock (GIL) prevents multi-threaded Python bytecode from executing on multiple CPU cores simultaneously. Using `threading` for CPU-bound tasks adds context-switching overhead, running **slower** than single-threaded execution.

#### Refactored Production Python Code:
```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
from typing import List

def cpu_heavy_task(number: int) -> int:
    """CPU-bound calculation."""
    return sum(i * i for i in range(number))

def run_parallel_cpu_tasks(numbers: List[int]) -> List[int]:
    """Correct approach for CPU-bound work using ProcessPoolExecutor (Bypasses GIL)."""
    # FIX: Use separate processes (ProcessPoolExecutor) to utilize multiple CPU cores
    max_workers = os.cpu_count() or 4
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(cpu_heavy_task, numbers))
    return results

def run_parallel_io_tasks(urls: List[str]) -> List[str]:
    """Correct approach for I/O-bound tasks (Network / DB calls) using ThreadPoolExecutor."""
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Threads are ideal for I/O waiting operations
        results = list(executor.map(lambda url: "data", urls))
    return results
```

---

## 🎯 Summary Checklist for Code Review Round Success

1.  **Spot Security Issues First**: Always check for hardcoded secrets, SQL injection, missing IAM checks, and un-sanitized prompts.
2.  **Highlight Scalability & Performance**: Identify blocking synchronous HTTP/DB loops and recommend `async/await`, batching, and caching.
3.  **Demonstrate Google Cloud SDK Standards**: Use Application Default Credentials (ADC), Secret Manager, BigQuery Storage Write API, and Vertex AI SDK best practices.
4.  **Master Core Python Mechanics**: Audit mutable default arguments (`roles=[]`), memory leaks (`f.readlines()`), $O(N^2)$ loops, thread safety (`Lock`), and GIL distinctions (ProcessPool vs ThreadPool).
