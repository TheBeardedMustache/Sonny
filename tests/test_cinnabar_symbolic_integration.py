# Integration tests for symbolic resonance in Cinnabar modules
import os
import pytest
import openai

from backend.cinnabar.nlu import interpret_input
from backend.cinnabar.response import generate_response
from backend.core.core_agent import symbolic_state

class DummyResp:
    class Choice:
        def __init__(self, content):
            self.message = type('M', (), {'content': content})
    def __init__(self, content):
        self.choices = [self.Choice(content)]

@pytest.fixture(autouse=True)
def clear_symbolic_state():
    # Clear state before each test
    symbolic_state.state.clear()
    yield

def test_interpret_input_symbolic_update(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    # Monkeypatch new SDK OpenAI.chat.completions.create
    from openai import OpenAI
    dummy_cmp = type('cmp', (), {'create': staticmethod(lambda **kwargs: DummyResp('parsed_intent'))})
    dummy_chat = type('Chat', (), {'completions': dummy_cmp})
    monkeypatch.setattr(OpenAI, 'chat', dummy_chat)
    result = interpret_input("Test input")
    assert result == "parsed_intent"
    state = symbolic_state.get_state()
    assert "interpret_input" in state
    assert state["interpret_input"] == "parsed_intent"

def test_generate_response_symbolic_update(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    # Monkeypatch new SDK OpenAI.chat.completions.create
    from openai import OpenAI
    dummy_cmp = type('cmp', (), {'create': staticmethod(lambda **kwargs: DummyResp('reply_text'))})
    dummy_chat = type('Chat', (), {'completions': dummy_cmp})
    monkeypatch.setattr(OpenAI, 'chat', dummy_chat)
    result = generate_response("Hello")
    assert result == "reply_text"
    state = symbolic_state.get_state()
    assert "generate_response" in state
    assert state["generate_response"] == "reply_text"