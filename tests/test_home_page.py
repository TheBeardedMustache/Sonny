"""Tests for frontend Home_Page content."""
import streamlit as st
import pytest

from frontend.Home_Page import main as home_page

def test_home_page_render(monkeypatch):
    # Monkeypatch Streamlit methods to ensure no errors
    monkeypatch.setattr(st, 'title', lambda x: None)
    monkeypatch.setattr(st, 'subheader', lambda x: None)
    monkeypatch.setattr(st, 'markdown', lambda x: None)
    monkeypatch.setattr(st, 'json', lambda x: None)
    # Should not raise
    home_page()