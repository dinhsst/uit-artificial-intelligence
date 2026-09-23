"""Minimal isolated runner boundary for local development.

The service rejects unsafe source patterns, runs only inside its own container,
and applies resource/output limits. Production deployments should additionally
apply a hardened runtime profile (read-only rootfs, dropped capabilities,
seccomp, no network and a non-root user).
"""
import os
import re
import resource
import subprocess
import tempfile
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title='CPP Atlas Code Runner', version='0.1.0')
MAX_SOURCE_BYTES = 32_000
MAX_OUTPUT_BYTES = 16_000
TIMEOUT_SECONDS = 3
CPU_SECONDS = 3
MEMORY_BYTES = 256 * 1024 * 1024
MAX_PROCESSES = 16
FORBIDDEN = re.compile(r"(#include\s*<\s*(filesystem|fstream|sys/socket|netinet|unistd|cstdlib)\s*>|system\s*\(|popen\s*\(|fork\s*\(|exec\w*\s*\(|/proc/|/etc/|\.\./)", re.I)

class RunRequest(BaseModel):
    code: str = Field(min_length=1, max_length=MAX_SOURCE_BYTES)
    stdin: str = Field(default='', max_length=8_000)

def _limits():
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_SECONDS, CPU_SECONDS))
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))
    resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))
    resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_OUTPUT_BYTES, MAX_OUTPUT_BYTES))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))

class RunResponse(BaseModel):
    status: str
    stdout: str = ''
    stderr: str = ''
    exit_code: int | None = None
    trace_available: bool = False
    trace_message: str = 'Execution trace is unavailable for arbitrary code.'

@app.get('/healthz')
def healthz(): return {'status': 'ok', 'service': 'code-runner', 'standard': 'C++17'}

@app.post('/run', response_model=RunResponse)
def run(request: RunRequest):
    if len(request.code.encode()) > MAX_SOURCE_BYTES or FORBIDDEN.search(request.code):
        return RunResponse(status='REJECTED', stderr='Source violates runner policy.')
    temp_kwargs = {'prefix': 'cpp-atlas-'}
    workspace = os.getenv('RUNNER_WORKDIR')
    if workspace and Path(workspace).is_dir():
        temp_kwargs['dir'] = workspace
    with tempfile.TemporaryDirectory(**temp_kwargs) as workdir:
        root=Path(workdir); source=root/'main.cpp'; binary=root/'main'
        source.write_text(request.code, encoding='utf-8')
        try:
            compile_result=subprocess.run(['g++','-std=c++17','-O2','-pipe',str(source),'-o',str(binary)],cwd=root,capture_output=True,text=True,timeout=TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            return RunResponse(status='TIMED_OUT',stderr='Compilation timed out.')
        except OSError:
            return RunResponse(status='RUNNER_ERROR',stderr='Compiler is temporarily unavailable.')
        if compile_result.returncode != 0:
            return RunResponse(status='COMPILE_ERROR',stderr=compile_result.stderr[-MAX_OUTPUT_BYTES:],exit_code=compile_result.returncode)
        try:
            result=subprocess.run([str(binary)],cwd=root,input=request.stdin,capture_output=True,text=True,timeout=TIMEOUT_SECONDS, preexec_fn=_limits)
        except subprocess.TimeoutExpired as exc:
            output=exc.stdout or ''
            if isinstance(output, bytes):
                output=output.decode('utf-8', errors='replace')
            return RunResponse(status='TIMED_OUT',stdout=output[-MAX_OUTPUT_BYTES:],stderr='Execution timed out.')
        except OSError:
            return RunResponse(status='RUNNER_ERROR',stderr='Program could not be started.')
        if result.returncode < 0 and abs(result.returncode) in (9, 24):
            return RunResponse(status='TIMED_OUT',stdout=result.stdout[-MAX_OUTPUT_BYTES:],stderr='Execution exceeded the CPU limit.',exit_code=result.returncode)
        return RunResponse(status='COMPLETED' if result.returncode == 0 else 'RUNTIME_ERROR',stdout=result.stdout[-MAX_OUTPUT_BYTES:],stderr=result.stderr[-MAX_OUTPUT_BYTES:],exit_code=result.returncode)
