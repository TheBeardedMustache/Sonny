"""
automation_template.py

Template for Pydantic-validated desktop automation functions:
Defines input models and actions for GUI interactions.

Usage Example:
```python
from automation_template import MoveMouseInput, move_mouse

params = MoveMouseInput(x=100, y=200, duration=0.5)
move_mouse(params.x, params.y, params.duration)
``` 
"""
import logging
import pyautogui
from pydantic import BaseModel, validator

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
    params = MoveMouseInput(x=x, y=y, duration=duration)
    logger.info(f"Moving mouse to ({params.x}, {params.y}) over {params.duration}s")
    pyautogui.moveTo(params.x, params.y, duration=params.duration)