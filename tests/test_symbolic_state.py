"""Tests for symbolic resonance state management."""
import pytest

from backend.core.core_agent import symbolic_state, SymbolicState

def test_symbolic_state_update_and_get():
    ss = SymbolicState()
    ss.update("event1", 123)
    ss.update("event2", {"a": 1})
    state = ss.get_state()
    assert state["event1"] == 123
    assert state["event2"] == {"a": 1}

def test_global_symbolic_state_monolithic():
    symbolic_state.update("test_event", "data")
    gs = symbolic_state.get_state()
    assert gs.get("test_event") == "data"