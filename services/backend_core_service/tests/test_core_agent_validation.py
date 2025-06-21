# Validation tests for core_agent/process_request using Pydantic
import pytest
import logging

from backend.core.core_agent import process_request

def test_process_request_empty_text(caplog):
    caplog.set_level(logging.ERROR)
    result = process_request("")
    assert result is None
    assert "Validation error in process_request" in caplog.text