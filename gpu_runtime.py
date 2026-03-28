"""
ARP v4 — RunPod GPU Runtime Integration

Provides cloud GPU access for heavy computation (AI Scientist, etc.)
when local GPU is unavailable.

Usage:
    from gpu_runtime import RunPodGPU
    
    gpu = RunPodGPU(api_key="your-runpod-key")
    gpu.start_container()
    gpu.run("python3 train.py --epochs 100")
    gpu.stop()
"""

import json
import time
import subprocess
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

@dataclass
class GPUInstance:
    """A RunPod GPU instance."""
    id: str
    name: str
    status: str
    cost_per_hour: float
    gpu_type: str
    docker_image: str = "runpod/pytorch:2.1.0-cuda12.1-cudnn8-runtime"

class RunPodGPU:
    """
    RunPod GPU runtime manager for ARP v4.
    
    Handles:
    - Container lifecycle (start/stop)
    - SSH-based code execution
    - File transfer
    - Job queuing
    
    Requirements:
    - RUNPOD_API_KEY environment variable or passed as argument
    - SSH key configured for passwordless auth
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        container_config: Optional[dict] = None
    ):
        import os
        self.api_key = api_key or os.environ.get("RUNPOD_API_KEY", "")
        self.base_url = "https://api.runpod.io/graphql"
        
        self.container_config = container_config or {
            "gpu": "NVIDIA RTX 3090",
            "gpu_count": 1,
            "container_disk_in_gb": 50,
            "docker_image": "runpod/pytorch:2.1.0-cuda12.1-cudnn8-runtime",
            "env": {
                "PYTORCH_VERSION": "2.1.0",
                "CUDA_VERSION": "12.1",
            }
        }
        
        self.instance = None
        self.is_running = False
        
    def _graphql(self, query: str, variables: dict = None) -> dict:
        """Execute a GraphQL query against RunPod API."""
        import os
        
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
            
        result = subprocess.run(
            ["curl", "-s", "-X", "POST",
             "-H", f"Authorization: Bearer {self.api_key}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(payload),
             self.base_url],
            capture_output=True,
            text=True,
            cwd=os.path.expanduser("~")
        )
        
        return json.loads(result.stdout)
    
    def start(self, name: str = "arp-v4-gpu") -> GPUInstance:
        """
        Start a GPU container on RunPod.
        
        Returns:
            GPUInstance object with connection details
        """
        print(f"🚀 Starting RunPod GPU container: {name}")
        
        mutation = """
        mutation startContainer($input: PodCreateInput!) {
            podCreate(input: $input) {
                id
                name
                status
                costPerHr
                runtime
                gpuCount
                machine {
                    gpuDisplayName
                }
            }
        }
        """
        
        variables = {
            "input": {
                "name": name,
                "input": {
                    "gpuType": self.container_config["gpu"],
                    "gpuCount": self.container_config["gpu_count"],
                    "containerDiskInGb": self.container_config["container_disk_in_gb"],
                    "dockerImage": self.container_config["docker_image"],
                    "env": self.container_config.get("env", {}),
                }
            }
        }
        
        result = self._graphql(mutation, variables)
        
        if "errors" in result:
            raise Exception(f"Failed to start container: {result['errors']}")
            
        data = result["data"]["podCreate"]
        
        self.instance = GPUInstance(
            id=data["id"],
            name=data["name"],
            status=data["status"],
            cost_per_hour=data["costPerHr"],
            gpu_type=data["machine"]["gpuDisplayName"]
        )
        
        print(f"  Container ID: {self.instance.id}")
        print(f"  GPU: {self.instance.gpu_type}")
        print(f"  Status: {self.instance.status}")
        
        # Wait for container to be ready
        self._wait_for_ready()
        
        return self.instance
    
    def _wait_for_ready(self, timeout: int = 300):
        """Wait for container to be in RUNNING state."""
        print("  Waiting for container to be ready...")
        
        query = """
        query getPod($podId: String!) {
            pod(input: {podId: $podId}) {
                id
                status
                ip
            }
        }
        """
        
        start = time.time()
        while time.time() - start < timeout:
            result = self._graphql(query, {"podId": self.instance.id})
            
            if "errors" not in result:
                pod = result["data"]["pod"]
                if pod and pod["status"] == "RUNNING":
                    self.instance.ip = pod["ip"]
                    self.is_running = True
                    print(f"  ✅ Container ready! IP: {getattr(self.instance, 'ip', 'N/A')}")
                    return
                    
            time.sleep(5)
            
        raise Exception("Container failed to start within timeout")
    
    def execute(self, command: str, timeout: int = 3600) -> dict:
        """
        Execute a command on the GPU container via SSH.
        
        Args:
            command: The command to execute
            timeout: Max execution time in seconds
            
        Returns:
            Dict with stdout, stderr, return_code
        """
        if not self.is_running:
            raise Exception("Container not running. Call start() first.")
        
        # For RunPod Serverless, use the execute endpoint
        mutation = """
        mutation executeCommand($input: ExecutorInput!) {
            executeCommand(input: $input) {
                status
                output
            }
        }
        """
        
        # Actually, RunPod has different APIs:
        # - Serverless: /v1/run (async execution)
        # - Dedicated GPU: SSH-based execution
        
        # For now, use a simpler approach with subprocess SSH
        ssh_host = f"root@{getattr(self.instance, 'ip', '')}"
        
        result = subprocess.run(
            ["ssh", "-o", "StrictHostKeyChecking=no",
             "-o", "ConnectTimeout=10",
             ssh_host, command],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        }
    
    def copy_file(self, local_path: str, remote_path: str):
        """Copy a file to the GPU container."""
        if not self.is_running:
            raise Exception("Container not running")
            
        ssh_host = f"root@{getattr(self.instance, 'ip', '')}"
        
        subprocess.run([
            "scp", "-o", "StrictHostKeyChecking=no",
            local_path, f"{ssh_host}:{remote_path}"
        ], check=True)
    
    def copy_directory(self, local_dir: str, remote_dir: str):
        """Copy a directory to the GPU container."""
        if not self.is_running:
            raise Exception("Container not running")
            
        ssh_host = f"root@{getattr(self.instance, 'ip', '')}"
        
        subprocess.run([
            "scp", "-r", "-o", "StrictHostKeyChecking=no",
            local_dir, f"{ssh_host}:{remote_dir}"
        ], check=True)
    
    def stop(self):
        """Stop the GPU container."""
        if not self.instance:
            return
            
        print(f"🛑 Stopping container: {self.instance.id}")
        
        mutation = """
        mutation stopContainer($input: PodEndInput!) {
            podTerminate(input: $input) {
                id
                status
            }
        }
        """
        
        self._graphql(mutation, {"input": {"podId": self.instance.id}})
        
        self.is_running = False
        self.instance = None
        print("  ✅ Container stopped")
    
    def get_status(self) -> str:
        """Get current container status."""
        if not self.instance:
            return "Not started"
            
        query = """
        query getPod($podId: String!) {
            pod(input: {podId: $podId}) {
                status
                costPerHr
                uptimeInSeconds
            }
        }
        """
        
        result = self._graphql(query, {"podId": self.instance.id})
        
        if "errors" in result:
            return "Unknown"
            
        pod = result["data"]["pod"]
        return f"Status: {pod['status']}, Cost: ${pod['costPerHr']}/hr"


# ─── Serverless Mode (No SSH) ────────────────────────────────────────────────

class RunPodServerless:
    """
    RunPod Serverless GPU for one-shot executions.
    
    Better for short jobs that don't need persistent container.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        import os
        self.api_key = api_key or os.environ.get("RUNPOD_API_KEY", "")
        self.endpoint_url = "https://api.runpod.io/v1"
    
    def run(
        self,
        script: str,
        input_data: dict = None,
        gpu: str = "NVIDIA RTX 3090",
        timeout: int = 300
    ) -> dict:
        """
        Run a Python script on serverless GPU.
        
        Args:
            script: Python code to execute
            input_data: Dict to pass as JSON
            gpu: GPU type (RTX 3090, A100, etc.)
            timeout: Max execution time
            
        Returns:
            Execution result
        """
        import urllib.request
        import base64
        
        # Encode script
        encoded_script = base64.b64encode(script.encode()).decode()
        
        payload = {
            "input": {
                "script": encoded_script,
                "input_data": input_data or {},
            },
            "webhook": {
                "endpoint": "https://your-webhook.com/results"
            }
        }
        
        # For actual RunPod serverless, you'd use their SDK
        # This is a simplified mock for the interface
        
        print(f"🚀 Submitting serverless job...")
        print(f"   GPU: {gpu}")
        print(f"   Timeout: {timeout}s")
        
        return {
            "status": "submitted",
            "message": "Use RunPod SDK for actual serverless execution"
        }


# ─── AI Scientist Integration ─────────────────────────────────────────────────

class AIScientistRunner:
    """
    Run AI Scientist on RunPod GPU.
    
    Handles:
    - Clone/setup AI Scientist repo
    - Execute experiments
    - Retrieve results
    """
    
    def __init__(self, gpu: RunPodGPU):
        self.gpu = gpu
        
    def setup(self, repo_url: str = "https://github.com/SakanaAI/AI-Scientist.git"):
        """Setup AI Scientist on GPU container."""
        print("📦 Setting up AI Scientist on GPU...")
        
        commands = [
            f"git clone {repo_url} /workspace/AI-Scientist",
            "cd /workspace/AI-Scientist",
            "pip install -r requirements.txt",
            "apt-get update && apt-get install -y texlive-full",
        ]
        
        for cmd in commands:
            print(f"  Running: {cmd[:50]}...")
            result = self.gpu.execute(cmd, timeout=600)
            if result["return_code"] != 0:
                print(f"  ⚠️ Warning: {result['stderr'][:200]}")
                
        print("  ✅ AI Scientist ready")
    
    def run_experiment(
        self,
        experiment: str,
        model: str = "gpt-4o-2024-05-13",
        num_ideas: int = 2
    ) -> dict:
        """
        Run an AI Scientist experiment.
        
        Args:
            experiment: Experiment template (nanoGPT_lite, 2d_diffusion, grokking)
            model: LLM model to use
            num_ideas: Number of ideas to generate
            
        Returns:
            Experiment results
        """
        print(f"🧪 Running AI Scientist experiment...")
        print(f"   Template: {experiment}")
        print(f"   Model: {model}")
        print(f"   Ideas: {num_ideas}")
        
        command = f"""
        cd /workspace/AI-Scientist && \
        python launch_scientist.py \
            --model "{model}" \
            --experiment {experiment} \
            --num-ideas {num_ideas}
        """
        
        result = self.gpu.execute(command, timeout=3600)
        
        return {
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "return_code": result["return_code"]
        }
    
    def retrieve_papers(self, output_dir: str = "/workspace/AI-Scientist/generated_papers") -> list:
        """Retrieve generated papers."""
        result = self.gpu.execute(f"ls -la {output_dir}")
        return result["stdout"]


# ─── Convenience Functions ─────────────────────────────────────────────────────

def quick_run(script: str, gpu_type: str = "NVIDIA RTX 3090") -> dict:
    """
    Quick serverless GPU execution.
    
    Simple interface for one-shot GPU tasks.
    """
    print(f"🚀 Quick GPU run on {gpu_type}")
    print(f"   Script length: {len(script)} chars")
    
    # This would use RunPod's serverless endpoint
    # For now, return mock response
    return {
        "status": "ready",
        "message": "Configure RUNPOD_API_KEY for actual execution"
    }


def check_gpu_availability() -> dict:
    """Check which GPUs are available on RunPod."""
    # Placeholder - would call RunPod API
    return {
        "rtx_3090": {"available": True, "price_per_hour": 0.40},
        "rtx_4090": {"available": True, "price_per_hour": 0.50},
        "a100": {"available": True, "price_per_hour": 1.50},
        "h100": {"available": True, "price_per_hour": 3.00},
    }
