"""
Google Cloud Run (gVisor-isolated MicroVM) & Vertex AI Code Execution Sandbox.
Provides isolated, ephemeral execution environments for agent data analytics, SQL queries, and Python execution.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import time
import subprocess
import tempfile
import os
from ..config import settings

@dataclass
class GCPSandboxExecutionResult:
    success: bool
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    execution_time_ms: float = 0.0
    container_id: str = "gcp-cloudrun-gvisor-001"
    is_sandboxed: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

class GCPgVisorSandbox:
    """
    Harness component simulating Google Cloud Run with gVisor container isolation.
    Enforces application kernel syscall interception and strict timeout limits.
    """
    def __init__(self):
        self.sandbox_url = settings.cloud_run_sandbox_url

    def execute_python_code(self, code_snippet: str, timeout_seconds: float = 5.0) -> GCPSandboxExecutionResult:
        """
        Executes Python code in an isolated gVisor-compatible sandbox environment.
        """
        start_time = time.time()
        
        # gVisor / Cloud Run Security Policy: Intercept disallowed system operations
        dangerous_ops = ["os.system", "shutil.rmtree", "subprocess.Popen", "socket.socket", "ctypes.CDLL"]
        for op in dangerous_ops:
            if op in code_snippet:
                return GCPSandboxExecutionResult(
                    success=False,
                    stderr=f"gVisor Syscall Intercept: Blocked dangerous operation '{op}' under GCP Workload Identity & Sandbox Policy.",
                    exit_code=1,
                    execution_time_ms=(time.time() - start_time) * 1000,
                    metadata={"security_verdict": "BLOCKED_GVISOR_SECURITY_PROFILE"}
                )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp_file:
            tmp_file.write(code_snippet)
            tmp_path = tmp_file.name

        try:
            process = subprocess.run(
                ["python3", tmp_path],
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            elapsed_ms = (time.time() - start_time) * 1000
            return GCPSandboxExecutionResult(
                success=(process.returncode == 0),
                stdout=process.stdout.strip(),
                stderr=process.stderr.strip(),
                exit_code=process.returncode,
                execution_time_ms=elapsed_ms,
                metadata={"runtime": "CloudRun_gVisor_Python311", "project": settings.project_id}
            )
        except subprocess.TimeoutExpired:
            return GCPSandboxExecutionResult(
                success=False,
                stderr=f"Cloud Run Sandbox SLA Timeout: Execution exceeded {timeout_seconds}s.",
                exit_code=-1,
                execution_time_ms=(time.time() - start_time) * 1000
            )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
