"""Integration tests for combined Silver and Gold automation capabilities."""
import os
import pyautogui
import pytest
from backend.core.core_agent import SilverAutomation, GoldAutomation

def test_silver_and_gold_instantiation():
    sa = SilverAutomation()
    ga = GoldAutomation()
    assert hasattr(sa, 'move_mouse')
    assert hasattr(sa, 'click')
    assert hasattr(ga, 'generate_script')
    assert hasattr(ga, 'modify_script')

def test_combined_workflow(monkeypatch):
    # Monkeypatch PyAutoGUI and Codex API
    calls = []
    monkeypatch.setattr(pyautogui, 'click', lambda x, y, button='left': calls.append(('click', x, y, button)))
    from backend.core.codex_auto import generate_script
    monkeypatch.setattr('backend.core.codex_auto.generate_script', lambda prompt, model, max_tokens: 'print(\'ok\')')
    # Perform a click
    sa = SilverAutomation()
    sa.click(0, 0)
    # Generate script
    ga = GoldAutomation()
    code = ga.generate_script('Test prompt')
    assert code.strip().startswith('print')
    assert calls == [('click', 0, 0, 'left')]