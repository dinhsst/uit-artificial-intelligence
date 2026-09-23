from dataclasses import dataclass
import json
import logging
import httpx
from .config import get_settings

logger=logging.getLogger('cpp-atlas.api')

@dataclass
class RunnerResult:
    status: str
    stdout: str = ''
    stderr: str = ''
    exit_code: int | None = None
    trace_available: bool = False
    trace_message: str = 'Execution trace is unavailable for arbitrary code.'

async def run_code(code: str, stdin: str) -> RunnerResult:
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            response=await client.post(f'{get_settings().runner_url}/run',json={'code':code,'stdin':stdin})
            response.raise_for_status()
            payload=response.json()
            if not isinstance(payload, dict) or not isinstance(payload.get('status'), str):
                raise ValueError('Runner response has an invalid shape')
            stdout=payload.get('stdout', '')
            stderr=payload.get('stderr', '')
            trace_available=payload.get('trace_available', False)
            trace_message=payload.get('trace_message', RunnerResult.__dataclass_fields__['trace_message'].default)
            if not isinstance(stdout, str) or not isinstance(stderr, str) or not isinstance(trace_available, bool) or not isinstance(trace_message, str):
                raise ValueError('Runner response has invalid field types')
            exit_code=payload.get('exit_code')
            if exit_code is not None and not isinstance(exit_code, int):
                raise ValueError('Runner response has an invalid exit code')
            return RunnerResult(status=payload['status'], stdout=stdout, stderr=stderr, exit_code=exit_code, trace_available=trace_available, trace_message=trace_message)
    except (httpx.HTTPError, OSError):
        return RunnerResult(status='RUNNER_UNAVAILABLE',stderr='Code runner is temporarily unavailable.')
    except (json.JSONDecodeError, TypeError, ValueError, KeyError) as exc:
        logger.warning('Invalid response from code runner: %s', exc)
        return RunnerResult(status='RUNNER_INVALID_RESPONSE',stderr='Code runner returned an invalid response.')
