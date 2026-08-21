"""
===============================================================================
MULTI-SOURCE AUTOMATED EVENT PIPELINE (SharePoint, Azure DevOps, GitHub)
===============================================================================
Demonstrates real-time event dispatcher processing webhooks from:
1. SharePoint Online (Microsoft Graph API Webhooks)
2. Azure DevOps (Service Hooks git.push / wiki.updated)
3. GitHub Repositories (GitHub Webhooks push / gollum)
===============================================================================
"""

import hmac
import hashlib
import json
from typing import Dict, Any, List

class MultiSourceVectorIndex:
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}

    def upsert_chunks(self, chunks: List[Dict[str, Any]]):
        for c in chunks:
            self.store[c["chunk_id"]] = c
        print(f"    [Azure AI Search] Atomic Upsert ({len(chunks)} chunks) successful.")

    def purge_document(self, doc_id: str):
        keys_to_delete = [k for k, v in self.store.items() if v.get("doc_id") == doc_id]
        for k in keys_to_delete:
            del self.store[k]
        print(f"    [Azure AI Search] Purged {len(keys_to_delete)} stale chunks for doc_id: '{doc_id}'.")


class UnifiedEventDispatcher:
    def __init__(self, index: MultiSourceVectorIndex):
        self.index = index

    def process_sharepoint_webhook(self, payload: Dict[str, Any]):
        """Processes Microsoft Graph Change Notification Payload."""
        value = payload.get("value", [{}])[0]
        change_type = value.get("changeType", "updated")  # created, updated, deleted
        resource_id = value.get("resourceData", {}).get("id", "sp-item-101")
        file_name = "sharepoint_policy.docx"

        print(f"\n📢 [SharePoint Webhook Received] ChangeType: '{change_type}', ResourceID: '{resource_id}'")
        
        if change_type in ["created", "updated"]:
            self._execute_upsert(source="SharePoint", file_name=file_name, doc_id=resource_id)
        elif change_type == "deleted":
            self.index.purge_document(doc_id=resource_id)

    def process_azure_devops_service_hook(self, payload: Dict[str, Any]):
        """Processes Azure DevOps Service Hook Event (git.push / wiki.updated)."""
        event_type = payload.get("eventType", "git.push")
        doc_id = "ado-wiki-arch-doc"
        file_name = "devops_architecture.md"

        print(f"\n📢 [Azure DevOps Service Hook] EventType: '{event_type}', File: '{file_name}'")
        
        if event_type in ["git.push", "wiki.page.updated"]:
            self._execute_upsert(source="AzureDevOps", file_name=file_name, doc_id=doc_id)
        elif event_type == "wiki.page.deleted":
            self.index.purge_document(doc_id=doc_id)

    def process_github_webhook(self, payload: Dict[str, Any]):
        """Processes GitHub Webhook Event (push / gollum)."""
        event_header = payload.get("event_type", "push")
        doc_id = "github-repo-readme"
        file_name = "README.md"

        print(f"\n📢 [GitHub Webhook Received] Event: '{event_header}', File: '{file_name}'")
        
        if event_header in ["push", "gollum"]:
            self._execute_upsert(source="GitHub", file_name=file_name, doc_id=doc_id)
        elif event_header == "repository_deleted":
            self.index.purge_document(doc_id=doc_id)

    def _execute_upsert(self, source: str, file_name: str, doc_id: str):
        print(f"   [{source} Processing] Extracting content & running Vision OCR for embedded PDF images...")
        chunk = {
            "chunk_id": f"{doc_id}-chunk-1",
            "doc_id": doc_id,
            "source": source,
            "file_name": file_name,
            "content": f"Sample extracted content from {source} ({file_name}).\n[FIGURE_CAPTION: Diagram captured.]"
        }
        self.index.upsert_chunks([chunk])


def main():
    print("=========================================================================")
    print("🚀 Demonstrating Multi-Source Event Dispatcher (SharePoint, ADO, GitHub)")
    print("=========================================================================")

    index = MultiSourceVectorIndex()
    dispatcher = UnifiedEventDispatcher(index)

    # 1. Simulate SharePoint Webhook Event
    sp_payload = {
        "value": [{
            "changeType": "updated",
            "subscriptionId": "sub-12345",
            "resourceData": {"id": "sp-drive-item-889"}
        }]
    }
    dispatcher.process_sharepoint_webhook(sp_payload)

    # 2. Simulate Azure DevOps Service Hook Event
    ado_payload = {
        "eventType": "wiki.page.updated",
        "publisherId": "tfs",
        "resource": {"path": "/Wikis/Architecture.md"}
    }
    dispatcher.process_azure_devops_service_hook(ado_payload)

    # 3. Simulate GitHub Webhook Event
    github_payload = {
        "event_type": "push",
        "repository": {"name": "agentic-rag-repo"},
        "commits": [{"modified": ["README.md"]}]
    }
    dispatcher.process_github_webhook(github_payload)

    print(f"\n[*] Total Active Vector Chunks in Index: {len(index.store)}")

    # 4. Simulate Deletion Event from SharePoint
    sp_delete_payload = {
        "value": [{
            "changeType": "deleted",
            "resourceData": {"id": "sp-drive-item-889"}
        }]
    }
    dispatcher.process_sharepoint_webhook(sp_delete_payload)

    print(f"[*] Total Active Vector Chunks after SharePoint Purge: {len(index.store)}")

    print("\n=========================================================================")
    print("✅ Multi-Source Event Dispatcher Pipeline Demos Completed!")
    print("=========================================================================")


if __name__ == "__main__":
    main()
