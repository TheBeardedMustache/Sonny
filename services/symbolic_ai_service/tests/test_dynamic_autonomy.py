"""Tests for dynamic autonomy enhancements (Animated Mercury)."""
import pytest

from backend.core.core_agent import AnimatedMercury, symbolic_state

@pytest.fixture(autouse=True)
def clear_state():
    symbolic_state.state.clear()
    yield

def test_generate_proactive_task(monkeypatch):
    # Stub LLMClient.chat
    monkeypatch.setattr('backend.cinnabar.base.LLMClient.chat', lambda self, text: 'next_task()')
    am = AnimatedMercury(symbolic_state=symbolic_state)
    task = am.generate_proactive_task()
    assert task == 'next_task()'
    state = symbolic_state.get_state()
    assert state.get('proactive_task') == 'next_task()'