import os
from backend.core.core_agent import run_agent, GoldAutomation
import pytest

def test_run_agent_returns_none(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    assert run_agent() is None

def test_gold_generate_script(monkeypatch):
    dummy_code = "print('hello')"
    monkeypatch.setattr("backend.core.codex_auto.generate_script", lambda prompt, model, max_tokens: dummy_code)
    result = GoldAutomation().generate_script("desc", model="test", max_tokens=10)
    assert result == dummy_code

def test_gold_modify_script(monkeypatch):
    calls = {}
    def fake_mod(path, instructions, model, max_tokens):
        calls["path"] = path
        calls["instructions"] = instructions
    monkeypatch.setattr("backend.core.codex_auto.modify_script", fake_mod)
    ga = GoldAutomation()
    ga.modify_script("file.py", "Add function", model="test", max_tokens=10)
    assert calls == {"path": "file.py", "instructions": "Add function"}

def test_gold_run_codex_cli(monkeypatch):
    expected = "ok"
    monkeypatch.setattr("backend.core.codex_auto.run_codex_cli", lambda command, cwd=None: expected)
    result = GoldAutomation().run_codex_cli(["codex", "--help"])
    assert result == expected