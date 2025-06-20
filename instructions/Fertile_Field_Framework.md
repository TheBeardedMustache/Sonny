# Fertile Field Framework
This document outlines Sonny's robust modular architecture and guides future expansions.

## Core Layers
1. **Mercury (Streamlit Frontend)**
   - `frontend/components/`: Modular UI components (home, silver, gold, cinnabar, combined).
   - `frontend/app.py`: Main application tying components to sidebar navigation.

2. **Regulus (Stable Core Logic)**
   - `backend/core/`:
     - `core_agent.py`: Agent wrappers (`SilverAutomation`, `GoldAutomation`, `AnimatedMercury`) and `SymbolicState`.
     - `core_tasks.py`: Pydantic-validated automation functions for GUI tasks.
     - `core_utils.py`: Utility helpers.

3. **Cinnabar (Advanced Symbolic Reasoning)**
   - `backend/cinnabar/base.py`: `LLMClient` abstraction with validation, logging, and symbolic-state integration.
   - `nlu.py` & `response.py`: Specialized clients for interpretation and response generation.

4. **API Layer**
   - `backend/api.py`: FastAPI endpoints (`/process/`, `/` healthcheck).

5. **Containerization**
   - `Dockerfile` & `docker-compose.yml`: Secure, resource-constrained deployment images and configurations.

## Templates and Reusable Modules
- `residual_modules/`: Distilled reusable modules (symbolic state, LLM client, automation).
- `fresh_regulus_templates/`: Foundational agent wrapper template.
- `frontend/components/`: Reusable UI component templates.

## Best Practices
- **Validation**: Use Pydantic for all external inputs.
- **Logging**: Centralize structured logs with context and symbolic-state updates.
- **Modularity**: Keep UI, core logic, and LLM integration in separate modules.
- **Testing**: Cover units, integration, symbolic flows, and load scenarios.
- **Security**: Load secrets via `.env`, limit container resources, enable healthchecks.

By following this blueprint, developers can safely extend Sonny with new autonomous agents and interactive capabilities.