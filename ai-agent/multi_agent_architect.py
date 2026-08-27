import os
import asyncio
from google.antigravity import Agent, LocalAgentConfig, types
from dotenv import load_dotenv

load_dotenv()

class MultiAgentArchitect:
    def __init__(self):
        # Configure the Supervisor Agent with capabilities to delegate tasks to subagents
        self.supervisor_config = LocalAgentConfig(
            system_instructions=(
                "You are an Elite GCP Enterprise Architect (Supervisor Agent). "
                "You coordinate complex cloud migration and architectural sizing requests. "
                "You do not perform detailed cost calculations or security rule audits yourself. "
                "Instead, you must delegate these tasks to specialized subagents:\n"
                "1. Delegate GCE/GKE compute sizing and hosting cost estimations to a 'Cost Sizing Subagent'.\n"
                "2. Delegate IAM policy designs, firewall targets, and data encrypting keys definitions to a 'Security Sizing Subagent'.\n"
                "Once you receive their respective outputs, compile and synthesize them into a single, cohesive "
                "Enterprise Architecture Report containing an Sizing Estimate section and a Security Baseline section."
            ),
            capabilities=types.CapabilitiesConfig(
                enable_subagents=True  # Enables Agent-to-Agent (A2A) subagent delegation
            )
        )

    async def execute_workflow(self, prompt: str):
        """Runs the supervisor multi-agent coordination loop and streams responses and thoughts."""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            yield {"type": "text", "content": "Error: GEMINI_API_KEY environment variable not found. Please set it."}
            return

        try:
            # Instantiate supervisor agent
            async with Agent(config=self.supervisor_config) as supervisor:
                response = await supervisor.chat(prompt)
                
                # Stream supervisor internal reasoning (thoughts) showing delegation planning
                async for thought in response.thoughts:
                    if thought.strip():
                        yield {"type": "thought", "content": thought}

                # Stream the synthesized final response report
                async for chunk in response:
                    if chunk:
                        yield {"type": "text", "content": chunk}
                        
        except Exception as e:
            yield {"type": "text", "content": f"\nExecution Error: {str(e)}"}
