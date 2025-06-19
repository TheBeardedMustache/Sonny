# Sonny

Sonny is a powerful integrated agent platform offering:

- **Silver Path: Desktop Automation** using PyAutoGUI for mouse, keyboard, and OS interactions.
- **Gold Path: Autonomous Coding** leveraging OpenAI/Codex API and Codex CLI for script generation and modification.
- **Combined Regulus**: Seamlessly blend desktop automation and autonomous coding for end-to-end workflows.

## Features

### Desktop Automation (Silver)
- move_mouse(x, y, duration): Move cursor.
- click(x, y, button): Click at position.
- drag_mouse(x, y, duration): Drag cursor.
- type_text(text, interval): Type strings.
- press_keys(*keys): Send keyboard shortcuts.
- open_application(path): Launch applications.
- manage_window(action, window_title): Window management placeholder.

### Autonomous Coding (Gold)
- generate_script(prompt, model, max_tokens): Generate new Python scripts.
- modify_script(file_path, instructions, model, max_tokens): Refine existing scripts.
- run_codex_cli(command, cwd): Execute Codex CLI.

## Setup
1. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   pytest
   ```

## Usage
Invoke Silver or Gold paths programmatically via `backend.core.core_agent.SilverAutomation` and `GoldAutomation`.