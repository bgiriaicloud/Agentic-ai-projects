# Automated Event-Driven Data Pipeline for Azure Agentic RAG
## Real-Time Document Synchronization (Upload, Update, Delete)

This guide presents an enterprise architecture and implementation design for an **Automated Event-Driven Ingestion Pipeline** on Azure. It ensures that whenever documents (`.md`, `.pdf`, `.docx`) are uploaded, modified, or deleted in storage, the **Azure AI Search Vector Index** is updated in real-time within seconds without manual pipeline execution.

---

## 📋 Table of Contents
* [Section 1: Event-Driven Pipeline Architecture Diagram](#section-1-event-driven-pipeline-architecture-diagram)
* [Section 2: Azure Event Grid & Serverless Function Triggers](#section-2-azure-event-grid--serverless-function-triggers)
* [Section 3: Real-Time Event Handlers: Create, Update & Delete](#section-3-real-time-event-handlers-create-update--delete)
* [Section 4: Self-Healing Nightly Delta Sync Timer](#section-4-self-healing-nightly-delta-sync-timer)
* [Section 5: Monitoring, Alerting & Error DLQ Handling](#section-5-monitoring-alerting--error-dlq-handling)

---

## Section 1: Event-Driven Pipeline Architecture Diagram

![Automated Event-Driven RAG Pipeline Architecture](file:///Users/biswanathgiri/.gemini/antigravity-ide/brain/9783c67e-1064-4e7d-8c3e-892122e2efed/automated_event_driven_rag_pipeline_architecture_1787248370708.jpg)

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AZURE BLOB STORAGE CONTAINER                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ User Uploads / Updates / Deletes File: document1.pdf, spec.md, contract.docx                │  │
│  └───────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────┼────────────────────────────────────────────────────┘
                                               │
                       ┌───────────────────────┴───────────────────────┐
                       ▼                                               ▼
     [Event: BlobCreated / BlobModified]                 [Event: BlobDeleted]
                       │                                               │
                       ▼                                               ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               AZURE EVENT GRID MESSAGING LAYER                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Emits System Event Payload (Blob URL, Event Type, Content Length, Timestamp)               │  │
│  └───────────────────────────────────────────┬─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────┼────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           AZURE FUNCTION SERVERLESS EVENT HANDLER                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Python Event Handler (Determines Event Type -> Dispatches to Processing Pipeline)           │  │
│  └───────────────┬───────────────────────────────────────────────────────────┬─────────────────┘  │
└──────────────────┼───────────────────────────────────────────────────────────┼────────────────────┘
                   │                                                           │
        (On Created / Modified)                                          (On Deleted)
                   │                                                           │
                   ▼                                                           ▼
┌─────────────────────────────────────┐                     ┌─────────────────────────────────────┐
│ 1. Azure AI Doc Intelligence Layout │                     │ 1. Query Azure AI Search for All    │
│ 2. GPT-4o Vision OCR PDF Figures    │                     │    Chunks matching 'file_name'       │
│ 3. Format-Aware Chunking            │                     │ 2. Execute Batch Document Purge     │
│ 4. text-embedding-3-large Vector    │                     │    from Index                       │
└──────────────────┬──────────────────┘                     └──────────────────┬──────────────────┘
                   │                                                           │
                   ▼                                                           ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            AZURE AI SEARCH INDEX SYNCHRONIZATION                                  │
│  ┌─────────────────────────────────┐                     ┌─────────────────────────────────┐  │
│  │ Atomic Index Upsert             │                     │ Immediate Index Deletion        │  │
│  │ ('mergeOrUpload' batch)         │                     │ ('delete' batch)                │  │
│  └─────────────────────────────────┘                     └─────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Section 2: Azure Event Grid & Serverless Function Triggers

### 1. Event Grid Subscription Setup

Azure Event Grid listens for storage events on the container level and routes event JSON payloads to an Azure Function endpoint.

#### System Events Subscribed:
*   `Microsoft.Storage.BlobCreated` (New file upload)
*   `Microsoft.Storage.BlobRenamed` (File rename)
*   `Microsoft.Storage.BlobDeleted` (File deletion)

#### Sample Event Grid Payload (JSON)
```json
{
  "topic": "/subscriptions/0000-0000/resourceGroups/my-rg/providers/Microsoft.Storage/storageAccounts/mystorage",
  "subject": "/blobServices/default/containers/documents/blobs/architecture_spec.pdf",
  "eventType": "Microsoft.Storage.BlobCreated",
  "eventTime": "2026-08-20T23:22:00Z",
  "id": "e4a2b910-1234-5678-90ab-cdef12345678",
  "data": {
    "api": "PutBlob",
    "contentType": "application/pdf",
    "contentLength": 245890,
    "url": "https://mystorage.blob.core.windows.net/documents/architecture_spec.pdf"
  }
}
```

---

## Section 3: Real-Time Event Handlers: Create, Update & Delete

### 1. Document Creation / Modification Handler (`BlobCreated` / `BlobModified`)

When a file is uploaded or updated:
1.  **Download Blob**: Stream file bytes from Azure Blob Storage.
2.  **Multimodal Extraction**:
    *   *If `.pdf`*: Extract text/tables via Azure AI Document Intelligence + run GPT-4o Vision on embedded figures.
    *   *If `.md`*: Parse Markdown headers using AST parser.
    *   *If `.docx`*: Extract paragraphs and tables.
3.  **Chunking & Embedding**: Generate 3072-dimensional vector embeddings via `text-embedding-3-large`.
4.  **Atomic Index Upsert**: Execute `search_client.upload_documents(documents=chunks)` using `mergeOrUpload` mode. If chunks already exist for this document version, they are cleanly updated in-place.

---

### 2. Document Deletion Handler (`BlobDeleted`)

When a file is deleted from Azure Blob Storage:
1.  **Query Index for Document Chunks**: Search Azure AI Search index for all chunk documents matching `file_url` or `file_name`.
2.  **Execute Batch Delete**: Submit a deletion payload (`action="delete"`) containing matching `chunk_id` keys to purge stale vectors from the index immediately.

#### Python Event Handler Code Snippet
```python
from azure.search.documents import SearchClient

def handle_blob_deleted(search_client: SearchClient, deleted_file_url: str):
    """Purges all index chunks associated with a deleted blob file."""
    
    # 1. Search for all chunk IDs associated with the deleted file
    results = search_client.search(
        search_text="*",
        filter=f"file_url eq '{deleted_file_url}'",
        select=["chunk_id"]
    )
    
    chunk_ids_to_delete = [{"chunk_id": doc["chunk_id"], "@search.action": "delete"} for doc in results]
    
    if chunk_ids_to_delete:
        # 2. Execute batch index deletion
        result = search_client.index_documents(batch=chunk_ids_to_delete)
        print(f"Successfully purged {len(chunk_ids_to_delete)} index chunks for deleted file: {deleted_file_url}")
```

---

## Section 4: Self-Healing Nightly Delta Sync Timer

To guard against rare network drops or missed Event Grid webhooks, a **Nightly Timer Trigger (Cron: `0 0 2 * * *`)** executes a lightweight metadata audit:

```
[Nightly Delta Sync Cron @ 02:00 AM]
                  │
                  ▼
[1. Fetch All Active Storage Blob URLs + LastModified Timestamps]
                  │
                  ▼
[2. Fetch All Index Unique Source URLs + IndexTimestamps from Azure AI Search]
                  │
                  ▼
┌─────────────────┴─────────────────┐
│ Re-process Missing / Stale Blobs  │ ──> [Enqueues missed files to Processing Queue]
└───────────────────────────────────┘
```

---

## Section 5: Monitoring, Alerting & Error DLQ Handling

*   **Dead-Letter Queue (DLQ)**: If a malformed PDF causes Document Intelligence processing to fail, the Event Grid subscription automatically retries 3 times before routing the event to a Dead-Letter Blob Container (`documents-dlq`) for engineering inspection.
*   **Application Insights Alerts**: Triggers alerts if the Event Processing Queue exceeds 50 failed items or processing latency exceeds 30 seconds.
