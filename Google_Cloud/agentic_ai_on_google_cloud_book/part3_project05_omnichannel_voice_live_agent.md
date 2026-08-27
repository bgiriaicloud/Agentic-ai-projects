# Project 05: Omnichannel Customer Experience & Voice Live Agent

## 🎯 Executive Overview & Business Objective
A real-time, bidirectional voice and text customer service platform powered by Gemini 2.0 Live API, integrating with Contact Center AI (CCAI) and Cloud Spanner for sub-100ms conversational turnarounds.

---

## 🏗️ System Architecture

```
[Inbound Voice Call / Mobile App WebSocket Stream]
        │
        ▼ (Bidirectional Audio Stream)
[Cloud Run Live Audio Gateway]
        │
        ▼
[Gemini 2.0 Live Multimodal API (Direct Audio-to-Audio)]
        │
        ├─────────────────────────────┬─────────────────────────────┐
        ▼                             ▼                             ▼
[Cloud Spanner Session Store] [CCAI Dialogflow CX Routing] [CRM Lookup Tools]
```

---

## 💻 Production Implementation Code (Live Audio Session Initializer)

```python
import vertexai
from vertexai.generative_models import GenerativeModel

def initialize_customer_voice_session(session_id: str):
    """Initializes a low-latency live voice customer service session."""
    model = GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        system_instruction="You are a warm, helpful customer support representative for Google Cloud Enterprise."
    )
    chat = model.start_chat()
    print(f"✅ Voice Support Session Initialized for: {session_id}")
    return chat
```
