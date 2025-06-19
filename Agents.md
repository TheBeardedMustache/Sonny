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

## Gold Path: Autonomous Code Generation

Sonny can autonomously generate and modify Python scripts via the OpenAI/Codex API under supervision:

- generate_script(prompt, model, max_tokens): Generates a new Python script from a textual prompt.
- modify_script(file_path, instructions, model, max_tokens): Refines existing scripts per given instructions.
- run_codex_cli(command, cwd): Executes Codex CLI commands for advanced workflows.

 All operations include robust error handling and logging to ensure safe code modifications.

## Combined Path: Lunar Venusian Regulus

Sonny harmonizes desktop and coding automation into a unified workflow:

- Instantiates SilverAutomation to perform PyAutoGUI-driven interactions (mouse, keyboard, apps).
- Leverages GoldAutomation to generate or refine Python scripts on the fly via Codex CLI.
- Allows sequences like generating a tool script and then executing GUI tasks to deploy it.

The combined system logs every step and gracefully handles errors, providing a “beautiful violet sheen” of capabilities.