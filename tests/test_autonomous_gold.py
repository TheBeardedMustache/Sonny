"""Tests for AutonomousAgent dynamic coding capabilities."""
import pytest

from backend.core.autonomous_agent import AutonomousAgent
from backend.core.core_agent import symbolic_state

@pytest.fixture(autouse=True)
def clear_state():
    symbolic_state.state.clear()
    yield

def test_generate_and_refine(monkeypatch):
    # Stub LLMClient.chat to return predictable responses
    responses = ["initial code", "refined code"]
    def fake_chat(self, text):
        return responses.pop(0)
    monkeypatch.setattr('backend.cinnabar.base.LLMClient.chat', fake_chat)
    agent = AutonomousAgent()
    refined = agent.generate_and_refine("Create function foo()")
    assert refined == "refined code"
    state = symbolic_state.get_state()
    assert state.get('initial_code') == "initial code"
    assert state.get('refined_code') == "refined code"

def test_proactive_workflow(monkeypatch):
    # Stub chat to return 'X'
    monkeypatch.setattr('backend.cinnabar.base.LLMClient.chat', lambda self, text: 'X')
    agent = AutonomousAgent()
    result = agent.proactive_workflow()
    assert result == 'X'