"""Tests for Streamlit expander-based Symbolic State displays."""
import streamlit as st
import pytest

from frontend.components.home import home_page
from frontend.components.silver import silver_ui
from frontend.components.gold import gold_ui
from frontend.components.cinnabar import cinnabar_ui
from frontend.components.combined import combined_ui

@pytest.fixture(autouse=True)
def patch_streamlit(monkeypatch):
    # Stub out necessary Streamlit functions
    for fn in ['title', 'subheader', 'markdown', 'header', 'number_input',
               'text_area', 'text_input', 'columns', 'button', 'success',
               'write', 'code', 'json', 'expander', 'write']:
        monkeypatch.setattr(st, fn, lambda *args, **kwargs: None)
    monkeypatch.setattr(st, 'columns', lambda *args, **kwargs: [lambda *a, **k: None]*len(args))
    yield

def test_home_page_expander_no_error():
    # Should not raise using expander
    home_page()

def test_silver_ui_expander_no_error():
    silver_ui()

def test_gold_ui_expander_no_error():
    gold_ui()

def test_cinnabar_ui_expander_no_error():
    cinnabar_ui()

def test_combined_ui_expander_no_error():
    combined_ui()