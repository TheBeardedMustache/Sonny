"""Final verification tests after triple refinement."""
import subprocess
import pytest

def test_pytest_suite_passes():
    # Ensure all tests pass
    result = subprocess.run(["pytest", "-q", "--disable-warnings", "--maxfail=1"], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr

def test_dockerfile_buildable(monkeypatch):
    # Simulate docker build if docker available
    try:
        result = subprocess.run(["docker", "build", "-t", "sonny", "."], capture_output=True, text=True, timeout=300)
        assert result.returncode == 0, result.stdout + result.stderr
    except FileNotFoundError:
        pytest.skip("Docker not available in this environment")