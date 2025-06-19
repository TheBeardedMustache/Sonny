# Blueprint: Extending Sonny’s Architecture

This document provides guidelines for building future autonomous agents upon Sonny’s modular framework.

## 1. Architecture Overview
Sonny consists of three main layers:

- **Backend/Core**: Stable foundational logic in `backend/core/` (Silver for GUI, Gold for coding).
- **Automation**: Domain-specific helpers in `automation/` for desktop or system interaction.
- **Frontend**: User-facing interface in `frontend/` powered by Streamlit.

## 2. Creating New Agents
1. **Define Core Logic**: In `backend/core/`, add new modules or classes following the Silver/Gold pattern.
2. **Implement Automation Helpers**: Place reusable scripts in `automation/` with clear logging and error handling.
3. **Write Tests**: In `tests/`, create pytest modules to cover new logic, mocking external dependencies.

## 3. Best Practices
- **Logging**: Use `logging.getLogger(__name__)` and central `basicConfig()` in main entry point.
- **Environment Variables**: Load via `python-dotenv`, avoid hardcoding secrets.
- **Error Handling**: Wrap I/O and API calls in `try/except` with `logger.exception()`.
- **Code Generation Safety**: Validate OpenAI responses before writing to disk.

## 4. Scalability Guidelines
- Modularize each agent with clear responsibilities.
- Leverage the existing `SilverAutomation` and `GoldAutomation` classes as templates.
- Extend tests to include integration and security checks.

By following this blueprint, developers can safely and responsibly create new autonomous agents building on Sonny’s unified automation pathways.