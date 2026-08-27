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
    # 1. Configure the Supervisor Agent with capabilities to spawn subagents
    config = LocalAgentConfig(
        system_instructions=(
            "You are a Senior Cloud Platform Architect (Supervisor Agent). "
            "You receive complex Cloud Deployment tasks from the user. "
            "You do not write all the code or details yourself. Instead, you delegate subtasks "
            "to specialized subagents (e.g. a Terraform Developer subagent to write infrastructure code, "
            "and a Security Officer subagent to audit permissions). "
            "Once you receive their outputs, aggregate and summarize them in a clean final report."
        ),
        capabilities=types.CapabilitiesConfig(
            enable_subagents=True,  # Crucial for Agent-to-Agent (A2A) delegation
        )
    )

    print("=== Initializing Google Antigravity Supervisor Agent (A2A Orchestration) ===")
    async with Agent(config=config) as agent:
        prompt = (
            "We need to deploy a secure Cloud Run service connected to a Cloud SQL database. "
            "Use a subagent to write the basic Terraform configuration for the Cloud Run service and Cloud SQL DB. "
            "Use another subagent to write the IAM roles needed for the Cloud Run service account to access the DB. "
            "Then, aggregate their outputs into a final deployment roadmap."
        )
        print(f"\nUser: {prompt}\n")

        print("--- Chatting with Supervisor Agent ---")
        print("Executing delegation workflow (the supervisor will spin up subagents to solve this task)...")
        response = await agent.chat(prompt)

        # Print the final aggregated output
        async for chunk in response:
            print(chunk, end="", flush=True)
        print("\n--- End of A2A Response ---\n")

if __name__ == "__main__":
    asyncio.run(main())
