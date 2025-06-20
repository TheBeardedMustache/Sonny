"""
automation.py

Reusable automation functions with Pydantic validation extracted from core_tasks.
"""
import logging
import pyautogui
from pydantic import BaseModel, validator, ValidationError

logger = logging.getLogger(__name__)

class MoveMouseInput(BaseModel):
    x: int
    y: int
    duration: float = 0.0

    @validator('x', 'y')
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("coordinates must be non-negative")
        return v

    @validator('duration')
    def non_negative_duration(cls, v):
        if v < 0:
            raise ValueError("duration must be non-negative")
        return v

def move_mouse(x: int, y: int, duration: float = 0.0):
    """Move mouse cursor to (x, y) over duration."""
    try:
        params = MoveMouseInput(x=x, y=y, duration=duration)
    except ValidationError as e:
        logger.error(f"Validation error in move_mouse: {e}")
        return
    logger.info(f"Moving mouse to ({params.x}, {params.y}) over {params.duration}s")
    pyautogui.moveTo(params.x, params.y, duration=params.duration)