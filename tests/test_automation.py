"""Tests for automation.desktop_env_access functionality."""
import pyautogui
import logging
from automation.desktop_env_access import access_desktop

def test_access_desktop_moves_mouse(monkeypatch):
    calls = []
    monkeypatch.setattr(pyautogui, 'moveTo', lambda x, y: calls.append((x, y)))
    access_desktop()
    assert calls == [(0, 0)]