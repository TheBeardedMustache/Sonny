# Red Work: Purified Gold Path Instructions
This document details advanced backend logic enhancements and autonomous symbolic intelligence refinements.

## AutonomousAgent Module
- File: `backend/core/autonomous_agent.py`
- Class: `AutonomousAgent`
  - `generate_and_refine(prompt: str) -> str`: Generates code based on prompt and refines it.
  - `proactive_workflow() -> str`: Creates prompts from current symbolic state to self-improve.

## Integration
1. Instantiate `AutonomousAgent` in your workflow:
   ```python
   from backend.core.autonomous_agent import AutonomousAgent
   agent = AutonomousAgent()
   code = agent.generate_and_refine("Implement feature X")
   ```
2. Use `proactive_workflow` for continuous improvement:
   ```python
   next_code = agent.proactive_workflow()
   ```

## Testing
Run `tests/test_autonomous_gold.py` to verify AutonomousAgent behaviors.

## Deployment
Ensure OpenAI API key is set in `.env`. Containerized via Docker for secure execution.