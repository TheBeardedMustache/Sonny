# core_tasks.py: Stable core task handling for Sonny.


import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
import os
import subprocess
import pyautogui

def handle_task(task):
    """Processes a given task for the Sonny agent."""
    logger.debug("handle_task called with: %s", task)
    logger.info("Handling task: %s", task)
    try:
        # Core task processing placeholder
        pass
    except Exception:
        logger.exception("Error while handling task: %s", task)
        raise
    
# PyAutoGUI-based automation functions
def move_mouse(x, y, duration=0):
    """Move mouse cursor to (x, y) over optional duration."""
    logger.info(f"move_mouse: moving to ({x}, {y}) over {duration}s")
    try:
        pyautogui.moveTo(x, y, duration=duration)
    except Exception:
        logger.exception("Error in move_mouse")
        raise

def click(x=None, y=None, button='left'):
    """Click mouse at (x, y) with specified button."""
    logger.info(f"click: button={button} at ({x}, {y})")
    try:
        pyautogui.click(x, y, button=button)
    except Exception:
        logger.exception("Error in click")
        raise

def drag_mouse(x, y, duration=0):
    """Drag mouse to (x, y) over optional duration."""
    logger.info(f"drag_mouse: dragging to ({x}, {y}) over {duration}s")
    try:
        pyautogui.dragTo(x, y, duration=duration)
    except Exception:
        logger.exception("Error in drag_mouse")
        raise

def type_text(text, interval=0):
    """Type text string with optional interval."""
    logger.info(f"type_text: typing '{text}'")
    try:
        pyautogui.typewrite(text, interval=interval)
    except Exception:
        logger.exception("Error in type_text")
        raise

def press_keys(*keys):
    """Press key combination."""
    logger.info(f"press_keys: {keys}")
    try:
        pyautogui.hotkey(*keys)
    except Exception:
        logger.exception("Error in press_keys")
        raise

def open_application(path):
    """Open an application by given path."""
    logger.info(f"open_application: {path}")
    try:
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
    # Implementation depends on window management libraries
