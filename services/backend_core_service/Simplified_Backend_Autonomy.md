## Simplified Backend Autonomy

### Overview

This backend service now operates as a clear, text-based autonomous agent:

- **Single input mode:** All commands are accepted strictly as plain text (task/natural language/command strings).
- **Explicit tool decision:** On each input, the agent uses an LLM classification prompt to choose precisely:
    - **CMD**: shell/system command simulation
    - **CODEX**: code/script generation or modification (simulated)
    - **SYMBOLIC**: general reasoning/analysis
- **Transparent reasoning:** Every step, tool choice, action, and outcome are both:
    - Logged to `backend_core_service/logs/autonomy_log.log`
    - Included in the returned value for UI/consumption
- **No ambiguous tools:** If the LLM response is unclear, fallback to symbolic (LLM).

### Log File
- Location: `backend_core_service/logs/autonomy_log.log`
- Format: Timestamped `[YYYY-MM-DD hh:mm:ss] message` (reasoning, decision, results)
- Example:
    ```
    [2024-06-22 14:12:11] Received input: Deploy the app to Heroku
    [2024-06-22 14:12:12] LLM classified input as: CODEX
    [2024-06-22 14:12:12] Tool selected: CODEX CLI
    [2024-06-22 14:12:13] Simulated Codex CLI output: # Here is a Python script to deploy...
    [2024-06-22 14:12:13] Outcome: [SIMULATED CODEX] Codex output: # Here is a Python script to deploy...
    ```
    
### API Contract
#### `AutonomousAgent.reason_decide_act(user_input: str) -> dict`
- Returns a dict with:
    - `'log'`: List of step-wise log messages (also logged in file)
    - `'decision'`: Selected tool type (CMD, CODEX, SYMBOLIC, etc)
    - `'result'`: Simulated result string
    - `'symbolic_state'`: Updated symbolic state

#### `AutonomousAgent.process_chat(chat: str) -> str`
- Accepts a chat/task string.
- Returns a multi-line string with explicit `[log] ...` lines and final tool/action/result summary.
- All steps and outcomes are logged to the main autonomy log.

### Safety
- Shell and Codex executions are simulated. For real execution, see `codex_auto.py` and ensure guarded, controlled subprocess logic.

---
**Deployment**: On FastAPI/Backend service startup, logs are written automatically for every autonomous_agent invocation.