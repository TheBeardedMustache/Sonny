# Integration test for process_request symbolic flow
import os
import pytest
from backend.core.core_agent import process_request, symbolic_state

@pytest.fixture(autouse=True)
def clear_state():
    symbolic_state.state.clear()
    yield

def test_process_request_full_symbolic(monkeypatch):
    # Stub interpret_input and generate_response
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    monkeypatch.setattr('backend.cinnabar.nlu.openai.ChatCompletion.create',
                        lambda **kwargs: type('R', (), {'choices': [type('C', (), {'message': type('M', (), {'content': 'intent_val'})})]})())
    monkeypatch.setattr('backend.cinnabar.response.openai.ChatCompletion.create',
                        lambda **kwargs: type('R', (), {'choices': [type('C', (), {'message': type('M', (), {'content': 'response_val'})})]})())
    result = process_request("hello world")
    assert result == 'response_val'
    state = symbolic_state.get_state()
    assert state.get('process_request_input') == 'hello world'
    assert state.get('process_request_intent') == 'intent_val'
    assert state.get('process_request_response') == 'response_val'