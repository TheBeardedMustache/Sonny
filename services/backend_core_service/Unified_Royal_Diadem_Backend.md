Unified Royal Diadem Backend: Explicit Integration of Gold, Silver, Cinnabar, Combined Logic
===========================================================================================

This document details the explicit backend agent unification and logging for Sonny's "Royal Diadem" state.

**Core File:** `backend/core/autonomous_agent.py`

## Unified Backend Logic

All backend actions funnel through a single `AutonomousAgent` interface:

1. **Silver Path:**
   - If a request is classified as OS/desktop/shell-interaction: use explicit CMD execution ("silver" logic)
   - Calls a safe shell executor with explicit structured logging
   - All actions and results are tagged `[SILVER]` in `autonomy_log.log`
2. **Gold Path:**
   - If the request is related to code (generate, modify, edit): uses Codex via `codex_auto` ("gold" logic)
   - Logs every generation action/result with `[GOLD]`
3. **Cinnabar Path:**
   - If neither of the above, responds with raw LLM ("cinnabar" logic)
   - All outputs are explicitly tagged `[CINNABAR]`
4. **Combined Path:**
   - The agent uses an LLM classifier prompt to select the path, logs tool choice and all results as `[COMBINED]`
   - Full input, tool decision, and outcome are always included

**Explicit Logging:**
- Every action, tool dispatch, and result is logged *at each step* to `logs/autonomy_log.log` for audit and transparency.
- Tags: `[SILVER]`, `[GOLD]`, `[CINNABAR]`, `[COMBINED]` are present for every respective stage/action in the log.

**API Entry:**
- The static `AutonomousAgent.process_chat()` is the unified way to trigger a new reasoning flow, returning a string-logged explanation and output.

**Testing/Validation:**
- Manual and integration tests should show explicit log entries for every backend invocation.
- Symbolic state is updated for every decision for frontend UI transparency.

---
The backend is thus a readable, fully transparent Python module with maximal clarity for all explicit automation and code/assistant logic.