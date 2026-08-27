"""
===============================================================================
AUTOMATED EVENT-DRIVEN RAG INGESTION PIPELINE
===============================================================================
Simulates real-time Azure Event Grid event handling for:
1. BlobCreated / BlobModified: Automatic extraction, chunking, embedding, & index upsert
2. BlobDeleted: Automatic index document purging
===============================================================================
"""

import time
import json
from typing import List, Dict, Any

class MockAzureAISearchIndex:
    def __init__(self):
        self.index_store: Dict[str, Dict[str, Any]] = {}

    def upsert_documents(self, documents: List[Dict[str, Any]]):
        """Simulates search_client.upload_documents with mergeOrUpload mode."""
        for doc in documents:
            chunk_id = doc["chunk_id"]
            self.index_store[chunk_id] = doc
        print(f"    [Index] Upserted {len(documents)} document chunks into Azure AI Search.")

    def delete_documents_by_file_url(self, file_url: str):
        """Simulates search_client.delete_documents based on file_url filter."""
        keys_to_delete = [
            chunk_id for chunk_id, doc in self.index_store.items()
            if doc.get("file_url") == file_url
        ]
        for k in keys_to_delete:
            del self.index_store[k]
        print(f"    [Index] Purged {len(keys_to_delete)} stale document chunks for deleted file: '{file_url}'.")


class AutomatedEventPipelineHandler:
    def __init__(self, search_index: MockAzureAISearchIndex):
        self.search_index = search_index

    def handle_event_grid_payload(self, event_payload: Dict[str, Any]):
        """Main entry point for processing Azure Event Grid system event payloads."""
        event_type = event_payload.get("eventType")
        data = event_payload.get("data", {})
        file_url = data.get("url", "")
        file_name = file_url.split("/")[-1] if file_url else "unknown"

        print(f"\n⚡ Received Event Grid Signal: '{event_type}'")
        print(f"   Target File: '{file_name}' ({file_url})")

        if event_type in ["Microsoft.Storage.BlobCreated", "Microsoft.Storage.BlobRenamed"]:
            self._on_blob_created_or_updated(file_name, file_url)
        elif event_type == "Microsoft.Storage.BlobDeleted":
            self._on_blob_deleted(file_url)
        else:
            print(f"   [Ignored] Unhandled event type: {event_type}")

    def _on_blob_created_or_updated(self, file_name: str, file_url: str):
        """Processes file upload/update: Extraction -> Chunking -> Embedding -> Index Upsert."""
        print("   [Pipeline] Running automated document extraction & Vision OCR...")
        
        # Simulate format-aware extraction
        extracted_text = f"Automated pipeline content extracted from {file_name}."
        if file_name.endswith(".pdf"):
            extracted_text += "\n\n[FIGURE_CAPTION: Vision OCR captured system architecture diagram.]"

        # Simulate chunking & embedding creation
        chunks = [
            {
                "chunk_id": f"{file_name}-chunk-1",
                "file_name": file_name,
                "file_url": file_url,
                "content": extracted_text,
                "vector": [0.012, -0.045, 0.089] * 1024  # 3072 dims
            }
        ]

        # Atomic index upsert
        self.search_index.upsert_documents(chunks)

    def _on_blob_deleted(self, file_url: str):
        """Processes file deletion: Automatic index purge."""
        print("   [Pipeline] Initiating automated index cleanup...")
        self.search_index.delete_documents_by_file_url(file_url)


def main():
    print("=========================================================================")
    print("🚀 Demonstrating Real-Time Automated Event-Driven RAG Ingestion Pipeline")
    print("=========================================================================")

    index = MockAzureAISearchIndex()
    handler = AutomatedEventPipelineHandler(index)

    # 1. Simulate File Upload Event
    create_event = {
        "eventType": "Microsoft.Storage.BlobCreated",
        "eventTime": "2026-08-20T23:22:00Z",
        "data": {
            "url": "https://mystorage.blob.core.windows.net/documents/architecture_v2.pdf",
            "contentLength": 542000
        }
    }
    handler.handle_event_grid_payload(create_event)
    print(f"   Current Index Size: {len(index.index_store)} chunks.")

    # 2. Simulate File Update Event
    update_event = {
        "eventType": "Microsoft.Storage.BlobCreated",
        "eventTime": "2026-08-20T23:25:00Z",
        "data": {
            "url": "https://mystorage.blob.core.windows.net/documents/architecture_v2.pdf",
            "contentLength": 580000
        }
    }
    handler.handle_event_grid_payload(update_event)
    print(f"   Current Index Size: {len(index.index_store)} chunks.")

    # 3. Simulate File Deletion Event
    delete_event = {
        "eventType": "Microsoft.Storage.BlobDeleted",
        "eventTime": "2026-08-20T23:30:00Z",
        "data": {
            "url": "https://mystorage.blob.core.windows.net/documents/architecture_v2.pdf"
        }
    }
    handler.handle_event_grid_payload(delete_event)
    print(f"   Current Index Size: {len(index.index_store)} chunks.")

    print("\n=========================================================================")
    print("✅ Real-Time Automated Event-Driven Pipeline Demos Completed!")
    print("=========================================================================")


if __name__ == "__main__":
    main()
