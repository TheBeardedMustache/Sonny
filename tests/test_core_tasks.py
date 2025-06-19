import os
import subprocess
import pyautogui
import pytest
from backend.core.core_tasks import (
    handle_task,
    move_mouse,
    click,
    drag_mouse,
    type_text,
    press_keys,
    open_application,
    manage_window,
)

def test_handle_task_returns_none():
    assert handle_task("sample_task") is None

def test_move_mouse(monkeypatch):
    calls = []
    monkeypatch.setattr(pyautogui, "moveTo", lambda x, y, duration=0: calls.append((x, y, duration)))
    move_mouse(10, 20, duration=0.5)
    assert calls == [(10, 20, 0.5)]

def test_click(monkeypatch):
    calls = []
    monkeypatch.setattr(pyautogui, "click", lambda x, y, button='left': calls.append((x, y, button)))
    click(5, 5, button="right")
    assert calls == [(5, 5, "right")]

def test_drag_mouse(monkeypatch):
    calls = []
    monkeypatch.setattr(pyautogui, "dragTo", lambda x, y, duration=0: calls.append((x, y, duration)))
    drag_mouse(1, 2, duration=0.2)
    assert calls == [(1, 2, 0.2)]

def test_type_text(monkeypatch):
    calls = []
    monkeypatch.setattr(pyautogui, "typewrite", lambda text, interval: calls.append((text, interval)))
    type_text("abc", interval=0.1)
    assert calls == [("abc", 0.1)]

def test_press_keys(monkeypatch):
    calls = []
    monkeypatch.setattr(pyautogui, "hotkey", lambda *keys: calls.append(keys))
    press_keys("ctrl", "a")
    assert calls == [("ctrl", "a")]

def test_open_application_windows(monkeypatch):
    calls = []
    monkeypatch.setattr(os, "startfile", lambda path: calls.append(path))
    open_application("dummy.exe")
    assert calls == ["dummy.exe"]

def test_open_application_unix(monkeypatch):
    calls = []
    monkeypatch.setattr(os, "name", "posix", raising=False)
    monkeypatch.setattr(subprocess, "Popen", lambda args: calls.append(tuple(args)))
    open_application("/usr/bin/app")
    assert calls == [("/usr/bin/app",)]

def test_manage_window_does_not_error():
    assert manage_window("action", "title") is None