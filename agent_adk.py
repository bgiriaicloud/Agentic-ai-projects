import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv

# Load local environment variables from .env if present
load_dotenv()

# Pre-execution check: Verify API Key is available
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("WARNING: GEMINI_API_KEY environment variable not found.")
    print("Please set the GEMINI_API_KEY environment variable or create a .env file.")
    print("You can get an API key from Google AI Studio: https://aistudio.google.com/app/api-keys\n")

# 1. Define a custom tool for the agent
def calculate_vm_cost(instance_count: int, hours: int, cost_per_hour: float = 0.10) -> str:
    """Calculates the estimated compute engine instance hosting cost.

    Args:
        instance_count: The number of virtual machine instances.
        hours: Total number of hours the virtual machines run.
        cost_per_hour: The hourly rate per instance. Defaults to $0.10.
    """
    total_cost = instance_count * hours * cost_per_hour
    return f"The estimated cost for running {instance_count} instance(s) for {hours} hours at ${cost_per_hour:.2f}/hr is ${total_cost:.2f}."

async def main():
    # 2. Configure the agent with persona instructions and tools
    # We leave the model unset to default to gemini-3.5-flash, or set it explicitly if needed.
    config = LocalAgentConfig(
        system_instructions=(
            "You are a Cloud Solutions Architect specializing in Google Cloud Platform (GCP). "
            "You help users size their environments, estimate costs, and design architectures. "
            "Always behave professionally, explain your reasoning, and use available tools to make accurate calculations."
        ),
        tools=[calculate_vm_cost],
    )

    print("=== Initializing Google Antigravity (ADK) Agent ===")
    async with Agent(config=config) as agent:
        prompt = "We want to host 5 web servers on GCE for a 30-day billing cycle (720 hours). Can you compute the estimate and recommend GCE sizing?"
        print(f"\nUser: {prompt}\n")

        print("--- Streaming Agent Reasoning (Thoughts) ---")
        response = await agent.chat(prompt)
        async for thought in response.thoughts:
            print(thought, end="", flush=True)
        print("\n--- End of Thoughts ---\n")

        print("--- Streaming Agent Response ---")
        async for chunk in response:
            print(chunk, end="", flush=True)
        print("\n--- End of Response ---\n")

if __name__ == "__main__":
    # Run the async main loop
    asyncio.run(main())
