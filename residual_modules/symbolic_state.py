"""
symbolic_state.py

Reusable SymbolicState module extracted from core logic.
"""
import logging

logger = logging.getLogger(__name__)

class SymbolicState:
    """Tracks symbolic events and their associated data."""
    def __init__(self):
        self.state = {}

    def update(self, event: str, data):
        """Record an event with associated data."""
        self.state[event] = data
        logger.info(f"SymbolicState updated: {event} = {data}")

    def get_state(self):
        """Retrieve a snapshot of the current symbolic state."""
        return dict(self.state)