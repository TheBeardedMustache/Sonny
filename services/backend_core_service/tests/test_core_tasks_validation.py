# Validation tests for core_tasks using Pydantic
import pytest
import logging

from backend.core.core_tasks import move_mouse, click, type_text

def test_move_mouse_invalid_negative_coordinates(caplog):
    caplog.set_level(logging.ERROR)
    result = move_mouse(-1, 0, duration=0)
    assert result is None
    assert "Validation error in move_mouse" in caplog.text

def test_click_invalid_button(caplog):
    caplog.set_level(logging.ERROR)
    result = click(0, 0, button="middle-click")
    assert result is None
    assert "Validation error in click" in caplog.text

def test_type_text_empty(caplog):
    caplog.set_level(logging.ERROR)
    result = type_text("", interval=0)
    assert result is None
    assert "Validation error in type_text" in caplog.text