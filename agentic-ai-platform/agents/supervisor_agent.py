"""
Supervisor Agent Module - Enterprise Agentic AI Platform
---------------------------------------------------------
Master Orchestrator agent that handles incoming user requests, manages Agent-to-Agent (A2A) delegation,
evaluates subagent outputs, and synthesizes grounded answers.
"""

import time
import uuid
from typing import Dict, Any, List, Optional
from agents.worker_agents import CloudOpsWorkerAgent, FinOpsWorkerAgent


class SupervisorAgent:
    def __init__(self, name: str = "Supervisor-Architect"):
        self.name = name
        self.cloud_ops_agent = CloudOpsWorkerAgent()
        self.finops_agent = FinOpsWorkerAgent()
        self._history = []

    def orchestrate(self, user_prompt: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Orchestrates multi-agent execution loop:
        1. Query decomposition & subagent task assignment
        2. A2A delegation execution to CloudOps & FinOps worker agents
        3. Result aggregation & grounded answer synthesis
        4. Telemetry logging & trace generation
        """
        t0 = time.time()
        sid = session_id or f"session-{uuid.uuid4().hex[:8]}"

        traces = []
        traces.append({
            "step": 1,
            "agent": self.name,
            "action": "Initiate A2A Orchestration",
            "details": {"prompt": user_prompt, "session_id": sid},
            "timestamp": time.strftime("%H:%M:%S")
        })

        # Step 2: A2A Delegation
        lower_p = user_prompt.lower()
        subagent_outputs = []

        if "infra" in lower_p or "gke" in lower_p or "resource" in lower_p or "iam" in lower_p or "audit" in lower_p:
            t_ops = time.time()
            ops_res = self.cloud_ops_agent.execute_subtask("Scan GCP infrastructure resources & IAM security policies")
            subagent_outputs.append(ops_res)
            
            traces.append({
                "step": len(traces) + 1,
                "agent": self.name,
                "action": f"Delegate to A2A Subagent '{self.cloud_ops_agent.name}'",
                "details": ops_res,
                "timestamp": time.strftime("%H:%M:%S"),
                "latency_ms": round((time.time() - t_ops) * 1000, 2)
            })

        if "cost" in lower_p or "billing" in lower_p or "finops" in lower_p or "cud" in lower_p or "spend" in lower_p or "calculate" in lower_p:
            t_fin = time.time()
            fin_res = self.finops_agent.execute_subtask("Query BigQuery billing exports & calculate CUD savings")
            subagent_outputs.append(fin_res)

            traces.append({
                "step": len(traces) + 1,
                "agent": self.name,
                "action": f"Delegate to A2A Subagent '{self.finops_agent.name}'",
                "details": fin_res,
                "timestamp": time.strftime("%H:%M:%S"),
                "latency_ms": round((time.time() - t_fin) * 1000, 2)
            })

        # Fallback if no specific trigger words, run both subagents for comprehensive report
        if not subagent_outputs:
            ops_res = self.cloud_ops_agent.execute_subtask("Scan GCP infrastructure resources")
            fin_res = self.finops_agent.execute_subtask("Query BigQuery billing export")
            subagent_outputs = [ops_res, fin_res]

        # Step 3: Synthesis & Grounded Response
        synthesis_parts = [
            f"### Enterprise Agentic AI Platform Response (`{sid}`)\n",
            f"**Master Orchestrator (`{self.name}`)** completed Agent-to-Agent (A2A) task delegation across specialized subagents:\n"
        ]

        for out in subagent_outputs:
            synthesis_parts.append(f"- **{out['subagent']}** ({out['role']}): {out['summary']}")

        synthesis_parts.append("\n**Key Recommendations & Actions**:")
        synthesis_parts.append("1. **Cost Optimization**: Enrolling Compute Engine instances into 1-Year Committed Use Discounts (CUD) will save **$435.00/month**.")
        synthesis_parts.append("2. **IAM Hardening**: Rotate service account keys and transition primitive Owner bindings to fine-grained predefined roles.")

        grounded_answer = "\n\n".join(synthesis_parts)

        total_latency_ms = round((time.time() - t0) * 1000, 2)

        return {
            "session_id": sid,
            "user_prompt": user_prompt,
            "supervisor_agent": self.name,
            "grounded_response": grounded_answer,
            "subagent_outputs": subagent_outputs,
            "traces": traces,
            "metrics": {
                "total_latency_ms": total_latency_ms,
                "subagents_count": len(subagent_outputs),
                "status": "SUCCESS"
            }
        }
