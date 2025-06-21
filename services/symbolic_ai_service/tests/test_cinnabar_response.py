import os
import openai
import pytest
import logging
from backend.cinnabar.response import generate_response

class DummyResp2:
    class Choice:
        def __init__(self, content):
            self.message = type("M", (), {"content": content})
    def __init__(self, content):
        self.choices = [self.Choice(content)]

def test_generate_response_success(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    # Monkeypatch new SDK OpenAI.chat.completions.create
    from openai import OpenAI
    dummy_cmp = type('cmp', (), {'create': staticmethod(lambda **kwargs: DummyResp2('reply_text'))})
    dummy_chat = type('Chat', (), {'completions': dummy_cmp})
    monkeypatch.setattr(OpenAI, 'chat', dummy_chat)
    result = generate_response("Hello")
    assert result == "reply_text"

def test_generate_response_no_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        generate_response("Hello")
    
def test_generate_response_empty_text(caplog):
    caplog.set_level(logging.ERROR)
    import pytest
    from backend.cinnabar.response import generate_response
    with pytest.raises(ValueError):
        generate_response("", model="gpt-4", max_tokens=10)
    assert "Validation error in generate_response" in caplog.text