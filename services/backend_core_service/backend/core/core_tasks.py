# core_tasks.py: Stable core task handling for Sonny.


import logging
import os
import subprocess
try:
    import pyautogui
except (KeyError, ImportError):
    pyautogui = None
from pydantic import BaseModel, ValidationError, validator
from backend.core.core_agent import symbolic_state

logger = logging.getLogger(__name__)

def handle_task(task):
    """Processes a given task for the Sonny agent."""
    logger.debug("handle_task called with: %s", task)
    logger.info("Handling task: %s", task)
    try:
        # Core task processing placeholder
        symbolic_state.update("handle_task", task)
        pass
    except Exception:
        logger.exception("Error while handling task: %s", task)
        raise
    
# PyAutoGUI-based automation functions
def move_mouse(x, y, duration=0):
    """Move mouse cursor to (x, y) over optional duration."""
    # Validate inputs
    class _MoveMouseInput(BaseModel):
        x: int
        y: int
        duration: float
        @validator('x', 'y')
        def non_negative_coords(cls, v):
            if v < 0:
                raise ValueError('coordinates must be non-negative')
            return v
        @validator('duration')
        def non_negative_duration(cls, v):
            if v < 0:
                raise ValueError('duration must be non-negative')
            return v
    try:
        _MoveMouseInput(x=x, y=y, duration=duration)
    except ValidationError as e:
        logger.error(f"Validation error in move_mouse: {e}")
        return None
    if pyautogui is None:
        raise RuntimeError("Desktop automation unavailable: missing DISPLAY or pyautogui installation.")
    logger.info(f"move_mouse: moving to ({x}, {y}) over {duration}s")
    try:
        symbolic_state.update("move_mouse", {"x": x, "y": y, "duration": duration})
        pyautogui.moveTo(x, y, duration=duration)
    except Exception:
        logger.exception("Error in move_mouse")
        raise

def click(x=None, y=None, button='left'):
    """Click mouse at (x, y) with specified button."""
    # Validate inputs
    class _ClickInput(BaseModel):
        x: int
        y: int
        button: str
        @validator('x', 'y')
        def non_negative_coords(cls, v):
            if v is None or v < 0:
                raise ValueError('coordinates must be non-negative')
            return v
        @validator('button')
        def valid_button(cls, v):
            if v not in ('left', 'right', 'middle'):
                raise ValueError('button must be left, right, or middle')
            return v
    try:
        _ClickInput(x=x, y=y, button=button)
    except ValidationError as e:
        logger.error(f"Validation error in click: {e}")
        return None
    if pyautogui is None:
        raise RuntimeError("Desktop automation unavailable: missing DISPLAY or pyautogui installation.")
    logger.info(f"click: button={button} at ({x}, {y})")
    try:
        symbolic_state.update("click", {"x": x, "y": y, "button": button})
        pyautogui.click(x, y, button=button)
    except Exception:
        logger.exception("Error in click")
        raise

def drag_mouse(x, y, duration=0):
    """Drag mouse to (x, y) over optional duration."""
    if pyautogui is None:
        raise RuntimeError("Desktop automation unavailable: missing DISPLAY or pyautogui installation.")
    logger.info(f"drag_mouse: dragging to ({x}, {y}) over {duration}s")
    try:
        symbolic_state.update("drag_mouse", {"x": x, "y": y, "duration": duration})
        pyautogui.dragTo(x, y, duration=duration)
    except Exception:
        logger.exception("Error in drag_mouse")
        raise

def type_text(text, interval=0):
    """Type text string with optional interval."""
    # Validate inputs
    class _TypeTextInput(BaseModel):
        text: str
        interval: float
        @validator('text')
        def non_empty_text(cls, v):
            if not v or not v.strip():
                raise ValueError('text cannot be empty')
            return v
        @validator('interval')
        def non_negative_interval(cls, v):
            if v < 0:
                raise ValueError('interval must be non-negative')
            return v
    try:
        _TypeTextInput(text=text, interval=interval)
    except ValidationError as e:
        logger.error(f"Validation error in type_text: {e}")
        return None
    if pyautogui is None:
        raise RuntimeError("Desktop automation unavailable: missing DISPLAY or pyautogui installation.")
    logger.info(f"type_text: typing '{text}'")
    try:
        symbolic_state.update("type_text", {"text": text, "interval": interval})
        pyautogui.typewrite(text, interval=interval)
    except Exception:
        logger.exception("Error in type_text")
        raise

def press_keys(*keys):
    """Press key combination."""
    logger.info(f"press_keys: {keys}")
    if pyautogui is None:
        raise RuntimeError("Desktop automation unavailable: missing DISPLAY or pyautogui installation.")
    try:
        symbolic_state.update("press_keys", {"keys": keys})
        pyautogui.hotkey(*keys)
    except Exception:
        logger.exception("Error in press_keys")
        raise

def open_application(path):
    """Open an application by given path."""
    logger.info(f"open_application: {path}")
    try:
        symbolic_state.update("open_application", {"path": path})
        if os.name == 'nt':
            os.startfile(path)
        else:
            subprocess.Popen([path])
    except Exception:
        logger.exception("Error in open_application")
        raise

def manage_window(action, window_title=None):
    """Manage window operations (placeholder)."""
    logger.info(f"manage_window: action={action}, window_title={window_title}")
    symbolic_state.update("manage_window", {"action": action, "window_title": window_title})
    # Implementation depends on window management libraries
