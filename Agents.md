# Agents
Documentation of available agents and their roles.

## Silver Path: Desktop Automation

Sonny can perform reliable desktop automation using PyAutoGUI, including:

- move_mouse(x, y, duration): Moves the mouse cursor to specified screen coordinates.
- click(x, y, button): Clicks the mouse at given position with specified button.
- drag_mouse(x, y, duration): Drags the mouse cursor to target coordinates.
- type_text(text, interval): Types the given string with optional key press interval.
- press_keys(*keys): Sends keyboard shortcut combinations.
- open_application(path): Opens an application by file path.
- manage_window(action, window_title): Placeholder for window management operations.