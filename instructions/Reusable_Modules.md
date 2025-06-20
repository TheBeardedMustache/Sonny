# Reusable Modules
This document lists and describes modular, reusable components extracted from Sonny’s core and Cinnabar logic for future projects.

## 1. SymbolicState (backend/core/core_agent.py)
- Tracks key events and associated data representing the agent’s symbolic reasoning.
- Methods:
  - `update(event: str, data)`: Record an event.
  - `get_state() -> dict`: Retrieve current symbolic state.

## 2. LLMClient & LLMRequest (backend/cinnabar/base.py)
- Encapsulates OpenAI ChatCompletion interactions with validation and symbolic-state integration.
- Classes:
  - `LLMRequest(BaseModel)`: Validates `text: str` input.
  - `LLMClient`: Handles system prompt, model, tokens, temperature, and logs requests/responses to `SymbolicState`.

## 3. Automation Functions & Input Models (backend/core/core_tasks.py)
- Pydantic-validated input models for GUI automation:
  - `MoveMouseInput(x: int, y: int, duration: float)`
  - `ClickInput(x: int, y: int, button: str)`
  - `TypeTextInput(text: str, interval: float)`
  - `PressKeysInput(keys: Tuple[str, ...])`
  - `OpenAppInput(path: str)`
  - `ManageWindowInput(action: str, window_title: Optional[str])`
- Corresponding functions:
  - `move_mouse(...)`, `click(...)`, `drag_mouse(...)`, `type_text(...)`, `press_keys(...)`, `open_application(...)`, `manage_window(...)`

## 4. Agent Wrappers (backend/core/core_agent.py)
- Provides high-level agent classes:
  - `SilverAutomation`: Methods for desktop actions, delegating to automation functions.
  - `GoldAutomation`: Methods for code generation and CLI interactions via LLMClient.
  - `process_request(text: str) -> str`: Orchestrates NLU interpretation and LLM response.

Each module above is designed for independent reuse. The following folders now contain reusable logic and templates:

- `residual_modules/`: distilled, production-ready modules:
  - `symbolic_state.py`
  - `llm_client.py`
  - `automation.py`
- `fresh_regulus_templates/`: foundational agent wrapper templates:
  - `agent_wrapper_template.py`

Refer to these directories for examples of how to integrate and reuse Sonny’s core components.