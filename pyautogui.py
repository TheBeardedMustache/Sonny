"""
Stub module for PyAutoGUI to satisfy imports during testing.
"""
def moveTo(x, y, duration=0, *args, **kwargs):
    """Stub for pyautogui.moveTo"""
    return None

def click(x=None, y=None, clicks=1, interval=0.0, button='left', *args, **kwargs):
    """Stub for pyautogui.click"""
    return None

def dragTo(x, y, duration=0, *args, **kwargs):
    """Stub for pyautogui.dragTo"""
    return None

def typewrite(message, interval=0.0, *args, **kwargs):
    """Stub for pyautogui.typewrite"""
    return None

def hotkey(*args, **kwargs):
    """Stub for pyautogui.hotkey"""
    return None