import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent_run import AgentOrchestrator
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GCP Agentic AI Platform Demo")

# Initialize our ADK Agent orchestrator
orchestrator = AgentOrchestrator()

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest):
    """Chat endpoint that executes the user prompt against the ADK Agent.

    It returns both the internal reasoning steps (thoughts) and the final response.
    """
    thoughts = []
    text_responses = []
    
    # Run the generator to collect thoughts and response chunks
    async for event in orchestrator.execute_query(payload.message):
        if event["type"] == "thought":
            thoughts.append(event["content"])
        elif event["type"] == "text":
            text_responses.append(event["content"])
            
    return {
        "status": "success",
        "thoughts": "".join(thoughts),
        "response": "".join(text_responses)
    }

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serves the premium dark glassmorphism testing dashboard."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GCP Agentic AI - Cloud Run Demo</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Mono&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-color: #0b0f19;
                --card-bg: rgba(17, 25, 40, 0.7);
                --border-color: rgba(255, 255, 255, 0.1);
                --text-color: #f3f4f6;
                --accent-cyan: #06b6d4;
                --accent-blue: #3b82f6;
                --thought-color: #a855f7;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: 'Outfit', sans-serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                background-image: 
                    radial-gradient(at 10% 20%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
                    radial-gradient(at 90% 80%, rgba(6, 182, 212, 0.15) 0px, transparent 50%);
            }

            header {
                padding: 1.5rem 2rem;
                border-bottom: 1px solid var(--border-color);
                backdrop-filter: blur(12px);
                background-color: rgba(11, 15, 25, 0.5);
                display: flex;
                justify-content: space-between;
                align-items: center;
                position: sticky;
                top: 0;
                z-index: 100;
            }

            .logo {
                font-weight: 800;
                font-size: 1.5rem;
                background: linear-gradient(to right, var(--accent-blue), var(--accent-cyan));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.5px;
            }

            .badge {
                background: rgba(6, 182, 212, 0.1);
                border: 1px solid var(--accent-cyan);
                color: var(--accent-cyan);
                padding: 0.25rem 0.75rem;
                border-radius: 9999px;
                font-size: 0.8rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            }

            main {
                flex-grow: 1;
                max-width: 1200px;
                width: 100%;
                margin: 2rem auto;
                padding: 0 1.5rem;
                display: grid;
                grid-template-columns: 1fr;
                gap: 2rem;
            }

            .chat-container {
                background: var(--card-bg);
                backdrop-filter: blur(16px);
                border: 1px solid var(--border-color);
                border-radius: 20px;
                padding: 2rem;
                display: flex;
                flex-direction: column;
                height: 600px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            }

            .chat-messages {
                flex-grow: 1;
                overflow-y: auto;
                margin-bottom: 1.5rem;
                padding-right: 0.5rem;
            }

            .message {
                margin-bottom: 1.5rem;
                max-width: 85%;
                line-height: 1.5;
            }

            .message.user {
                margin-left: auto;
                background: linear-gradient(135deg, var(--accent-blue), #2563eb);
                padding: 0.75rem 1.25rem;
                border-radius: 18px 18px 0 18px;
                box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
            }

            .message.agent {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid var(--border-color);
                padding: 1.25rem;
                border-radius: 18px 18px 18px 0;
            }

            .thought-box {
                background: rgba(168, 85, 247, 0.05);
                border-left: 3px solid var(--thought-color);
                padding: 0.75rem 1rem;
                margin-bottom: 1rem;
                border-radius: 0 8px 8px 0;
                font-family: 'Space Mono', monospace;
                font-size: 0.85rem;
                color: #d8b4fe;
                overflow-x: auto;
                white-space: pre-wrap;
            }

            .thought-title {
                font-weight: 600;
                font-size: 0.75rem;
                text-transform: uppercase;
                color: var(--thought-color);
                margin-bottom: 0.25rem;
                letter-spacing: 0.5px;
            }

            .input-area {
                display: flex;
                gap: 1rem;
            }

            textarea {
                flex-grow: 1;
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid var(--border-color);
                border-radius: 12px;
                padding: 0.75rem 1rem;
                color: var(--text-color);
                font-family: inherit;
                font-size: 1rem;
                resize: none;
                height: 50px;
                outline: none;
                transition: border-color 0.3s;
            }

            textarea:focus {
                border-color: var(--accent-cyan);
            }

            button {
                background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                padding: 0 2rem;
                cursor: pointer;
                transition: transform 0.2s, opacity 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            button:hover {
                transform: translateY(-2px);
                opacity: 0.95;
            }

            button:active {
                transform: translateY(0);
            }

            button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }

            footer {
                text-align: center;
                padding: 1.5rem;
                font-size: 0.85rem;
                color: rgba(255, 255, 255, 0.4);
                border-top: 1px solid var(--border-color);
                backdrop-filter: blur(12px);
            }

            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 6px;
            }
            ::-webkit-scrollbar-track {
                background: transparent;
            }
            ::-webkit-scrollbar-thumb {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        </style>
    </head>
    <body>
        <header>
            <div class="logo">Enterprise Agentic AI Platform</div>
            <div class="badge">Google Cloud Run Demo</div>
        </header>

        <main>
            <div class="chat-container">
                <div class="chat-messages" id="chat-messages">
                    <div class="message agent">
                        Hello! I am your GCP solutions assistant. I am backed by the **Google Antigravity SDK** and connected to an external knowledge base via **Model Context Protocol (MCP)**. Ask me about our GCP architecture standards, Cloud Run deployment guidelines, or Zero-Trust security rules!
                    </div>
                </div>
                <div class="input-area">
                    <textarea id="user-input" placeholder="Type your query (e.g. 'What are the rules for deploying Cloud Run?')"></textarea>
                    <button id="send-btn">Send Query</button>
                </div>
            </div>
        </main>

        <footer>
            Enterprise Agentic AI Platform • Developed using Google Antigravity SDK & Gemini
        </footer>

        <script>
            const chatMessages = document.getElementById('chat-messages');
            const userInput = document.getElementById('user-input');
            const sendBtn = document.getElementById('send-btn');

            userInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            sendBtn.addEventListener('click', sendMessage);

            async function sendMessage() {
                const messageText = userInput.value.trim();
                if (!messageText) return;

                // Disable UI
                userInput.value = '';
                userInput.disabled = true;
                sendBtn.disabled = true;

                // Append user message
                appendMessage(messageText, 'user');

                // Append temporary loading message
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'message agent';
                loadingDiv.id = 'temp-loading';
                loadingDiv.innerText = 'Consulting knowledge base and reasoning...';
                chatMessages.appendChild(loadingDiv);
                scrollToBottom();

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: messageText }),
                    });

                    const data = await response.json();
                    
                    // Remove loading indicator
                    document.getElementById('temp-loading').remove();

                    if (data.status === 'success') {
                        appendAgentResponse(data.thoughts, data.response);
                    } else {
                        appendMessage('Error processing request: ' + data.message, 'agent');
                    }
                } catch (error) {
                    document.getElementById('temp-loading').remove();
                    appendMessage('Network Error: ' + error.message, 'agent');
                }

                // Enable UI
                userInput.disabled = false;
                sendBtn.disabled = false;
                userInput.focus();
            }

            function appendMessage(text, sender) {
                const msgDiv = document.createElement('div');
                msgDiv.className = `message ${sender}`;
                msgDiv.innerText = text;
                chatMessages.appendChild(msgDiv);
                scrollToBottom();
            }

            function appendAgentResponse(thoughts, responseText) {
                const msgDiv = document.createElement('div');
                msgDiv.className = 'message agent';

                if (thoughts) {
                    const thoughtBox = document.createElement('div');
                    thoughtBox.className = 'thought-box';
                    thoughtBox.innerHTML = `<div class="thought-title">Agent Internal Reasoning (ADK Thoughts)</div>${thoughts}`;
                    msgDiv.appendChild(thoughtBox);
                }

                const responseContent = document.createElement('div');
                responseContent.innerText = responseText;
                msgDiv.appendChild(responseContent);

                chatMessages.appendChild(msgDiv);
                scrollToBottom();
            }

            function scrollToBottom() {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    import uvicorn
    # Use environment port for Cloud Run suitability
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
