"""
desktop.py: Desktop automation convenience wrappers using PyAutoGUI.
"""
import pyautogui

def move_mouse(x: int, y: int, duration: float = 0.0) -> None:
    """Move the mouse cursor to (x, y) over duration seconds."""
    pyautogui.moveTo(x, y, duration)

def click(x: int, y: int, button: str = 'left') -> None:
    """Click the mouse at (x, y) with the specified button."""
    pyautogui.click(x, y, button=button)