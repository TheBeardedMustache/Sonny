import os
from backend.core.core_agent import run_agent

def test_run_agent_returns_none(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    assert run_agent() is None