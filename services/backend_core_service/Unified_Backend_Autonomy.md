## Unified Backend Autonomy

### Overview
Sonny's backend logic for task automation, codegen, code-editing, shell/OS interaction, and symbolic reasoning is now cleanly unified within `autonomous_agent.py`.

### What Was Changed/Merged
- All major agent logic (Gold/CodeGen, Silver/Automation, Cinnabar/NLU, Combined integration) is now handled within a single `AutonomousAgent`.
- Singular routing: The agent uses a classifier prompt to **autonomously decide** whether to:
    - Run a shell/OS command (CMD, Silver-like)
    - Generate or edit code via Codex API (CODEX CLI, Gold-like)
    - Or default to symbolic LLM/assistant-style response (Cinnabar)

### Logging
- **All reasoning steps, actions, tool decisions, and results** are recorded in:
  - `backend_core_service/logs/autonomy.log`
    - `[timestamp] [AUTONOMY|LEVEL] ...`
- Command executions (if CMD is chosen) are also logged in `cmd_execution.log`.

### Usage
- The agent works as a single unified automation entrypoint for all path types (`CMD`, `CODEX`, or symbolic), keeping a deterministic and debuggable history for every interaction, error, and tool selection.

### Example Log
```
[2024-06-22 22:11:31] [AUTONOMY|INFO] LLM tool decision for 'ls -l': CMD
[2024-06-22 22:11:31] [AUTONOMY|CMD] Executing 'ls -l'
[2024-06-22 22:11:31] [AUTONOMY|RESULT] CMD execution done. Result: file1 file2 file3
[2024-06-22 22:11:31] [AUTONOMY|OUTCOME] Outcome: file1 file2 file3
```

---
**Location:**  
- Code: `backend_core_service/backend/core/autonomous_agent.py`
- Log:  `backend_core_service/logs/autonomy.log`
- Doc:  `Unified_Backend_Autonomy.md`

---
All code automation, LLM, and CLI tools are now orchestrated/observable from this single root agent, providing end-to-end auditability and reasoning transparency.