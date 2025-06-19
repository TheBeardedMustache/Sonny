"""Vigorous integration tests for frontend-backend interactions."""
import pytest
import streamlit as st

from frontend.app import silver_ui, gold_ui, cinnabar_ui, combined_ui, main as app_main
from backend.core.core_agent import SilverAutomation, GoldAutomation, process_request
from backend.core.core_tasks import move_mouse, click

class DummySA:
    def __init__(self):
        self.moves = []
        self.clicks = []
    def move_mouse(self, x, y, duration=0):
        self.moves.append((x, y, duration))
    def click(self, x, y, button='left'):
        self.clicks.append((x, y, button))

class DummyGA(GoldAutomation):
    def generate_script(self, *args, **kwargs):
        return "# code"
    def modify_script(self, *args, **kwargs):
        return None
    def run_codex_cli(self, *args, **kwargs):
        return "ok"

@pytest.fixture(autouse=True)
def patch_streamlit(monkeypatch):
    # Stub out Streamlit UI calls
    for func in ['title', 'subheader', 'markdown', 'header', 'number_input',
                 'text_area', 'text_input', 'radio', 'button', 'success',
                 'write', 'code', 'json', 'exception']:
        monkeypatch.setattr(st, func, lambda *args, **kwargs: None)
    # number_input and others default values
    monkeypatch.setattr(st, 'number_input', lambda *args, **kwargs: 0)
    monkeypatch.setattr(st, 'text_area', lambda *args, **kwargs: "test")
    monkeypatch.setattr(st, 'text_input', lambda *args, **kwargs: "gpt-4")
    monkeypatch.setattr(st, 'radio', lambda *args, **kwargs: "Combined")
    monkeypatch.setattr(st, 'button', lambda *args, **kwargs: False)
    yield

def test_silver_ui_no_buttons(monkeypatch):
    # No buttons pressed
    silver_ui()

def test_silver_ui_with_buttons(monkeypatch):
    sa = DummySA()
    monkeypatch.setattr('frontend.app.SilverAutomation', lambda: sa)
    # Simulate Move Mouse button
    calls = []
    monkeypatch.setattr(st, 'button', lambda label: label == "Move Mouse")
    silver_ui()
    assert sa.moves == [(0, 0, 0.0)]

def test_gold_ui(monkeypatch):
    ga = DummyGA()
    monkeypatch.setattr('frontend.app.GoldAutomation', lambda: ga)
    # Simulate Generate Script button
    monkeypatch.setattr(st, 'button', lambda label: label == "Generate Script")
    gold_ui()

def test_cinnabar_ui(monkeypatch):
    monkeypatch.setattr('frontend.app.process_request', lambda text: "resp")
    monkeypatch.setattr(st, 'button', lambda label: label == "Interpret Input")
    cinnabar_ui()

def test_combined_ui():
    combined_ui()

def test_app_main_runs(monkeypatch):
    # Test the app main with each choice
    for choice in ["Home", "Silver", "Gold", "Cinnabar", "Combined"]:
        monkeypatch.setattr(st, 'radio', lambda *args, **kwargs: choice)
        app_main()