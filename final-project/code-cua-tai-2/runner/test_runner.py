import subprocess
from fastapi.testclient import TestClient
import runner as runner_module
from runner import app

client = TestClient(app)

def test_health_and_cpp17():
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json()['standard'] == 'C++17'

def test_compiles_and_runs_simple_program():
    response = client.post('/run', json={'code': '#include <iostream>\nint main(){std::cout << 42;}'})
    assert response.status_code == 200
    assert response.json()['status'] == 'COMPLETED'
    assert response.json()['stdout'] == '42'

def test_rejects_process_and_network_primitives():
    response = client.post('/run', json={'code': '#include <cstdlib>\nint main(){system("id");}'})
    assert response.json()['status'] == 'REJECTED'

def test_reports_compile_errors():
    response = client.post('/run', json={'code': 'int main( {'})
    assert response.json()['status'] == 'COMPILE_ERROR'


def test_reports_compile_timeout(monkeypatch):
    real_run = runner_module.subprocess.run

    def timeout_compile(command, *args, **kwargs):
        if command[0] == 'g++':
            raise subprocess.TimeoutExpired(command, kwargs.get('timeout'))
        return real_run(command, *args, **kwargs)

    monkeypatch.setattr(runner_module.subprocess, 'run', timeout_compile)
    response = client.post('/run', json={'code': 'int main(){return 0;}'})
    assert response.status_code == 200
    assert response.json()['status'] == 'TIMED_OUT'
