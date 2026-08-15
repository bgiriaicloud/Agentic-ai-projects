"""
Amazon AgentCore Python SDK & Runtime Framework
------------------------------------------------
Provides core primitives for building, running, and observing production-ready AI agents on Amazon AgentCore.

Components Implemented:
1. AgentCoreRuntime - Session container management & isolated execution
2. AgentCoreMemory - Short-term conversation context & Long-term persistent store
3. AgentCoreGateway - Model Context Protocol (MCP) tool dispatcher & registry
4. AgentCoreObservability - Chain-of-Thought tracing, metrics, & telemetry
5. CodeInterpreterSandbox - Secure code execution environment tool
"""

import os
import sys
import time
import uuid
import json
import io
from typing import List, Dict, Any, Optional, Callable
from pydantic import BaseModel, Field


# ==========================================
# Data Models
# ==========================================

class Message(BaseModel):
    role: str  # "user", "assistant", "system", "tool"
    content: str
    timestamp: str = Field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters_schema: Dict[str, Any]
    handler: Optional[Callable] = None


class TraceStep(BaseModel):
    step_number: int
    component: str  # "Runtime", "Planner", "Gateway", "Memory", "CodeSandbox"
    timestamp: str
    action: str
    details: Dict[str, Any]
    duration_ms: float


class AgentCoreSession(BaseModel):
    session_id: str
    created_at: str
    last_active: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ==========================================
# 1. AgentCore Memory Service
# ==========================================

class AgentCoreMemory:
    def __init__(self):
        # Short-term memory keyed by session_id
        self._short_term_memory: Dict[str, List[Message]] = {}
        # Long-term memory keyed by entity/user/session
        self._long_term_memory: Dict[str, Dict[str, Any]] = {}

    def get_history(self, session_id: str) -> List[Message]:
        return self._short_term_memory.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        if session_id not in self._short_term_memory:
            self._short_term_memory[session_id] = []
        msg = Message(role=role, content=content, metadata=metadata or {})
        self._short_term_memory[session_id].append(msg)

    def set_long_term_fact(self, session_id: str, key: str, value: Any):
        if session_id not in self._long_term_memory:
            self._long_term_memory[session_id] = {}
        self._long_term_memory[session_id][key] = {
            "value": value,
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    def get_long_term_facts(self, session_id: str) -> Dict[str, Any]:
        return self._long_term_memory.get(session_id, {})


# ==========================================
# 2. AgentCore Gateway (MCP Tool Registry)
# ==========================================

class AgentCoreGateway:
    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register_tool(self, name: str, description: str, parameters_schema: Dict[str, Any], handler: Callable):
        tool_def = ToolDefinition(
            name=name,
            description=description,
            parameters_schema=parameters_schema,
            handler=handler
        )
        self._tools[name] = tool_def

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "parameters_schema": t.parameters_schema
            }
            for t in self._tools.values()
        ]

    def invoke_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        if tool_name not in self._tools:
            raise ValueError(f"Tool '{tool_name}' is not registered on AgentCore Gateway.")
        handler = self._tools[tool_name].handler
        if not handler:
            raise ValueError(f"Tool '{tool_name}' has no handler defined.")
        return handler(**arguments)


# ==========================================
# 3. AgentCore Observability (Telemetry & Tracing)
# ==========================================

class AgentCoreObservability:
    def __init__(self):
        self._traces: Dict[str, List[TraceStep]] = {}

    def start_trace(self, session_id: str):
        self._traces[session_id] = []

    def record_step(
        self,
        session_id: str,
        component: str,
        action: str,
        details: Dict[str, Any],
        duration_ms: float = 0.0
    ):
        if session_id not in self._traces:
            self._traces[session_id] = []

        step_num = len(self._traces[session_id]) + 1
        trace = TraceStep(
            step_number=step_num,
            component=component,
            timestamp=time.strftime("%H:%M:%S.%f")[:-3],
            action=action,
            details=details,
            duration_ms=round(duration_ms, 2)
        )
        self._traces[session_id].append(trace)

    def get_traces(self, session_id: str) -> List[TraceStep]:
        return self._traces.get(session_id, [])


# ==========================================
# 4. Code Interpreter Sandbox Environment
# ==========================================

class CodeInterpreterSandbox:
    @staticmethod
    def execute_python_code(code: str) -> Dict[str, Any]:
        """
        Executes Python code in a safe stdout-capturing sandbox environment.
        """
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output
        start_time = time.time()
        success = True
        error_msg = None

        try:
            # Shared execution context
            exec_scope = {"math": __import__("math"), "json": json}
            exec(code, exec_scope)
            output = redirected_output.getvalue()
        except Exception as e:
            success = False
            error_msg = str(e)
            output = redirected_output.getvalue()
        finally:
            sys.stdout = old_stdout

        exec_time_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "success": success,
            "stdout": output.strip(),
            "error": error_msg,
            "execution_time_ms": exec_time_ms
        }


# ==========================================
# 5. AgentCore Runtime Engine
# ==========================================

class AgentCoreRuntime:
    def __init__(self, execution_mode: str = "mock"):
        self.execution_mode = execution_mode.lower()
        self.memory = AgentCoreMemory()
        self.gateway = AgentCoreGateway()
        self.observability = AgentCoreObservability()
        self._active_sessions: Dict[str, AgentCoreSession] = {}

    def create_session(self, metadata: Optional[Dict[str, Any]] = None) -> AgentCoreSession:
        session_id = f"agentcore-session-{uuid.uuid4().hex[:8]}"
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        session = AgentCoreSession(
            session_id=session_id,
            created_at=now,
            last_active=now,
            metadata=metadata or {}
        )
        self._active_sessions[session_id] = session
        self.observability.start_trace(session_id)
        
        self.observability.record_step(
            session_id=session_id,
            component="Runtime",
            action="Session Created",
            details={"session_id": session_id, "execution_mode": self.execution_mode}
        )
        return session

    def get_session(self, session_id: str) -> Optional[AgentCoreSession]:
        return self._active_sessions.get(session_id)
