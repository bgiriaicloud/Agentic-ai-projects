import os
import sys
import asyncio
from google.antigravity import Agent, LocalAgentConfig, types

class AgentOrchestrator:
    def __init__(self):
        # Resolve the absolute path of mcp_server.py relative to this script
        self.mcp_script_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            "mcp_server.py"
        )
        
        # Define the stdio transport config to launch our local MCP server
        self.mcp_servers = [
            types.McpStdioServer(
                command="python3",
                args=[self.mcp_script_path]
            )
        ]
        
        # Configure the Google Antigravity Agent
        self.config = LocalAgentConfig(
            system_instructions=(
                "You are an expert Google Cloud Solutions Architect and FDE Assistant. "
                "Your job is to answer the user's questions about GCP deployments, networking, and security. "
                "You have access to an external GCP Knowledge Base through an MCP server. "
                "When asked about configurations, deployment guidelines, or compliance policies, "
                "always query the knowledge base first using available tools (like list_knowledge_topics "
                "and query_knowledge_base) to ground your answers in factual documentation. "
                "Synthesize the retrieved documentation into a clear, structured recommendation."
            ),
            mcp_servers=self.mcp_servers,
        )

    async def execute_query(self, user_prompt: str):
        """Executes a prompt against the ADK agent, yielding thoughts and final text responses.

        This is an async generator designed to support streaming.
        """
        # Pre-execution environment validation
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            yield {"type": "text", "content": "Error: GEMINI_API_KEY environment variable is not set. Please configure it to use Gemini."}
            return

        try:
            # Instantiate the Google Antigravity Agent
            async with Agent(self.config) as agent:
                response = await agent.chat(user_prompt)
                
                # 1. Stream agent reasoning (thoughts) to show model planning steps
                async for thought in response.thoughts:
                    # Filter empty thoughts to keep logs clean
                    if thought.strip():
                        yield {"type": "thought", "content": thought}

                # 2. Stream the final synthesized text chunks
                async for chunk in response:
                    if chunk:
                        yield {"type": "text", "content": chunk}
                        
        except Exception as e:
            yield {"type": "text", "content": f"\nExecution Error: {str(e)}"}
