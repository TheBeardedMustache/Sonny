import os
import openai
import pytest
import logging
from backend.cinnabar.nlu import interpret_input

class DummyResp:
    class Choice:
        def __init__(self, content):
            self.message = type("M", (), {"content": content})
    def __init__(self, content):
        self.choices = [self.Choice(content)]

def test_interpret_input_success(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    monkeypatch.setattr(openai.ChatCompletion, 'create', lambda **kwargs: DummyResp("parsed_intent"))
    result = interpret_input("Test input")
    assert result == "parsed_intent"

def test_interpret_input_no_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        interpret_input("Test")
    
def test_interpret_input_empty_text(caplog):
    caplog.set_level(logging.ERROR)
    import pytest
    from backend.cinnabar.nlu import interpret_input
    with pytest.raises(ValueError):
        interpret_input("", model="gpt-4", max_tokens=10)
    assert "Validation error in interpret_input" in caplog.text