"""
CLI Application Entry Point - Enterprise Agentic AI Platform
--------------------------------------------------------------
Usage:
  python3 main.py --query "Run cloud audit and finops cost calculation"
"""

import sys
import argparse
import json
from agents.supervisor_agent import SupervisorAgent

def main():
    parser = argparse.ArgumentParser(description="Enterprise Agentic AI Platform CLI")
    parser.add_argument("--query", type=str, default="Run full infrastructure audit and calculate BigQuery billing spend", help="User instruction prompt")
    args = parser.parse_args()

    print("\n=======================================================")
    print("      🚀 Enterprise Agentic AI Platform CLI            ")
    print("=======================================================\n")

    supervisor = SupervisorAgent()
    print(f"[*] Supervisor Agent '{supervisor.name}' initializing A2A orchestration...\n")

    res = supervisor.orchestrate(args.query)

    print("-------------------------------------------------------")
    print("GROUNDED RESPONSE:")
    print("-------------------------------------------------------")
    print(res["grounded_response"])
    print("\n-------------------------------------------------------")
    print("PERFORMANCE METRICS:")
    print(f"Total Latency: {res['metrics']['total_latency_ms']} ms")
    print(f"A2A Subagents Executed: {res['metrics']['subagents_count']}")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
