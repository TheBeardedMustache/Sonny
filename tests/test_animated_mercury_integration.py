"""End-to-end tests for dynamic autonomy and symbolic resonance (Philosophical Mercury)."""
import pytest

from frontend.components.combined import combined_ui
from backend.core.core_agent import AnimatedMercury, symbolic_state

@pytest.fixture(autouse=True)
def clear_state():
    symbolic_state.state.clear()
    yield

def test_animated_mercury_ui_and_logic(monkeypatch):
    # Patch AnimatedMercury to return a known task
    monkeypatch.setattr(AnimatedMercury, 'generate_proactive_task', lambda self: 'perform_action()')
    # Simulate Combined UI interpret
    monkeypatch.setattr('streamlit.button', lambda label: label == "Generate Proactive Task")
    monkeypatch.setattr('streamlit.json', lambda x: None)
    monkeypatch.setattr('streamlit.markdown', lambda x: None)
    monkeypatch.setattr('streamlit.header', lambda x: None)
    monkeypatch.setattr('streamlit.write', lambda x: None)
    combined_ui()
    state = symbolic_state.get_state()
    assert state.get('proactive_task') == 'perform_action()'