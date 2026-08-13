import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig, types
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()

# Pre-execution check: Verify API Key is available
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable not found.")
    print("Please set the GEMINI_API_KEY environment variable or create a .env file.")
    print("You can get an API key from Google AI Studio: https://aistudio.google.com/app/api-keys\n")

async def main():
    # 1. Define the Stdio connection configuration for our local MCP server
    # The server runs as "python3 mcp_server.py"
    # We use path resolver or relative execution for the mcp_server file.
    mcp_server_script = os.path.join(os.path.dirname(__file__), "mcp_server.py")
    
    mcp_servers = [
        types.McpStdioServer(
            command="python3",
            args=[mcp_server_script],
        )
    ]

    # 2. Configure the agent with the MCP server
    config = LocalAgentConfig(
        system_instructions=(
            "You are an operations assistant. You have access to a custom MCP server "
            "that lets you query GCP resources. When asked about GCP resources, use the "
            "list_gcp_resources tool to look them up."
        ),
        mcp_servers=mcp_servers,
    )

    print("=== Initializing Google Antigravity Agent with Custom MCP Server ===")
    print("Connecting to local MCP server via Stdio transport...")
    async with Agent(config=config) as agent:
        prompt = "What active Cloud Run services do we have in our production project?"
        print(f"\nUser: {prompt}\n")

        print("--- Chatting with Agent (resolving tool call to MCP Server) ---")
        response = await agent.chat(prompt)
        
        # Display response chunks
        async for chunk in response:
            print(chunk, end="", flush=True)
        print("\n--- End of Response ---\n")

        # Let's try another resource type
        prompt2 = "Can you check what GCS buckets are currently running?"
        print(f"User: {prompt2}\n")
        
        response2 = await agent.chat(prompt2)
        async for chunk in response2:
            print(chunk, end="", flush=True)
        print("\n--- End of Response ---\n")

if __name__ == "__main__":
    asyncio.run(main())
