## Command Line Autonomy: Sonny Backend

### Overview
Sonny now autonomously decides whether to execute command-line instructions or invoke code generation via Codex, with robust and secure logging.

### Secure CMD Handling
- When the agent's reasoning decides on **CMD**, the command is executed using Python's `subprocess` (via `run_cmd` utility).
- All commands, outputs, errors, and return codes are logged to:
  - `backend_core_service/logs/cmd_execution.log`
- Output and error handling is careful; failures and exceptions are captured and logged.

### Explicit Tool Reasoning
- **LLM-based decision step**: Each task is classified as requiring CMD (shell command), Codex (code generation), or Symbolic (general reasoning).
- All rationale and decisions are logged to:
  - `backend_core_service/logs/autonomy_log.log`

### Log Formats
- **autonomy_log.log:** Reasoning steps, e.g.:
  ```
  [2024-06-22 20:10:40] LLM classified input as: CMD
  [2024-06-22 20:10:40] Tool selected: CMD (Shell) for 'ls -l'
  [2024-06-22 20:10:42] CMD Execution complete for: 'ls -l'
  ```
- **cmd_execution.log:** Execution details, e.g.:
  ```
  [2024-06-22 20:10:41] CMD EXECUTE: ls -l
  [2024-06-22 20:10:41] OUTPUT: total 12 [...output...]
  [2024-06-22 20:10:41] ERROR: 
  [2024-06-22 20:10:41] RETURNCODE: 0
  ```

### Error Handling & Injection Safety
- Dangerous shell metacharacters should be considered when adapting for production.
- All subprocesses are limited in time and their output/exit code is always logged.

### Where This Happens
- Code: `backend/core/autonomous_agent.py`
- Docs: `Command_Line_Autonomy.md`
- Logs:  
  - `logs/cmd_execution.log` (CMDs)
  - `logs/autonomy_log.log` (Reasoning/decisions)

---
**Summary:**  
Sonny's backend is now capable of real, logged, and safe command execution and explicit reasoning between CMD and Codex pathways.