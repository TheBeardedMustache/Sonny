# Agents
Comprehensive overview of Sonny’s agent pathways and capabilities.

## Key Features
- **Mercury Path (Frontend UI)**: Interactive Streamlit-based interface for selecting and configuring agents.
- **Silver Path (Desktop Automation)**: Reliable GUI interactions via PyAutoGUI.
- **Gold Path (Autonomous Coding)**: Dynamic script generation and refinement via OpenAI Codex API and Codex CLI.
- **Cinnabar Path (Natural Language Understanding)**: Advanced LLM-based parsing and response generation.
- **Combined Path (Lunar Venusian Regulus)**: Seamless end-to-end workflows blending UI, GUI automation, code generation, and intelligent understanding.

## Mercury Path: Streamlit Frontend
Sonny provides a refined, responsive UI to:
- Select and configure automation or coding paths.
- Enter parameters (coordinates, prompts, file paths) with validation.
- Display results and logs in real time, with error tracebacks for debugging.

## Silver Path: Desktop Automation
Sonny can automate desktop environments with:
- move_mouse(x, y, duration): Move the cursor.
- click(x, y, button): Mouse clicks.
- drag_mouse(x, y, duration): Cursor dragging.
- type_text(text, interval): Automated typing.
- press_keys(*keys): Keyboard shortcuts.
- open_application(path): Launch applications.
- manage_window(action, window_title): Window management hooks.

## Gold Path: Autonomous Code Generation
Sonny can generate and update code safely:
- generate_script(prompt, model, max_tokens): Create new Python scripts.
- modify_script(file_path, instructions, model, max_tokens): Refine existing scripts.
- run_codex_cli(command, cwd): Execute Codex CLI commands.

## Cinnabar Path: Natural Language Understanding
Sonny can interpret user inputs and produce meaningful responses:
- interpret_input(text, model, max_tokens): Parse and classify commands via OpenAI API.
- generate_response(text, model, max_tokens): Craft assistant responses.

## Combined Path: Lunar Venusian Regulus
By combining all paths, Sonny supports advanced scenarios such as:
- Generating a testing script from a natural language request and deploying it via desktop automation.
- Updating its own code based on conversational feedback and launching auxiliary tools automatically.

All operations include robust error handling, logging, and environment isolation to ensure safety and maintainability.

## Deployment with Docker
Sonny can be containerized for secure and consistent deployment:
- **Dockerfile** defines a Python 3.11 slim environment.
- **Dependencies** are installed from `requirements.txt`.
- **Ports**: Streamlit UI is exposed on port `8501`.
- **Environment**: Use `--env-file .env` to pass sensitive keys securely.

## Symbolic Resonance
Sonny maintains a dynamic **SymbolicState** representing key events and reasoning flows:
- **SymbolicState.update(event, data)** records backend events (e.g., path executions, task parameters).
- **SymbolicState.get_state()** provides a real-time snapshot for debugging and UI display.
The Streamlit frontend automatically displays this state, reflecting Sonny’s internal symbolic reasoning.

## UI Symbolic Resonance Display
Each UI path (Silver, Gold, Cinnabar, Combined) now presents the current `SymbolicState` as a JSON panel, providing seamless insight into Sonny’s internal reasoning and fostering transparency.

## Structured Validation & Cleansing
To ensure resilience against invalid inputs, Sonny uses **Pydantic** models across backend components:
- **Input validation**: All user-provided parameters (coordinates, text, prompts) are parsed and validated via Pydantic.
- **Error logging**: Validation errors are logged with clear messages before any action is taken.
- **Cleansing & recovery**: Invalid inputs are automatically rejected or sanitized, maintaining stable operation.
This robust validation pipeline runs at every stage: frontend → backend → LLM integrations.

## Deployment with Docker
Sonny can be containerized for secure deployment:
- **Dockerfile** built on Python 3.11-slim.
- **Dependencies** installed from `requirements.txt`, including Pydantic, FastAPI, and Uvicorn.
- **Ports**: Streamlit UI on `8501`, FastAPI API on `8000`.
- **Secure env**: Launch with `--env-file .env` to pass sensitive keys.

> _Sonny’s architecture stands as a foundational framework for future autonomous agents, reflecting a “beautiful violet sheen” of cohesive automation logic._