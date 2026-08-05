import pytest
import subprocess

def test_cli_audit_e2e():
    result = subprocess.run(['python', 'main.py', 'audit', 'examples/package.json'], capture_output=True, text=True)
    assert result.returncode == 0
    assert 'react' in result.stdout or 'allowed' in result.stdout