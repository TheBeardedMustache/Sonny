## Unified Symbolic AI Integration

### Overview
The Symbolic AI service in Sonny now directly interfaces with the unified backend autonomy agent for all symbolic and natural language understanding tasks. Symbolic requests are routed robustly and reasoning path is logged for full transparency and debugging.

### What was changed
- **API unified:** Symbolic AI now exposes a single endpoint `/symbolic/` (POST) accepting a text payload for any symbolic, NLU, or reasoning request.
- **Backend autonomy integration:** All symbolic requests are routed to Sonny's unified `AutonomousAgent`, which decides (and logs) the best tool or reasoning path in the backend.
- **Explicit logging:** All symbolic requests, backend results, and key reasoning and tool decisions are structured-logged in `symbolic_ai_service/logs/symbolic_reasoning.log`.

### Example API Use
```python
POST /symbolic/
{ "text": "Summarize the importance of symbolic logic in AI." }
```
Yields backend-robust reasoning and result via a unified pathway, logged as:
```
[2024-06-22 22:20:51] [SYMBOLIC-AI|INFO] API /symbolic/ called with: 'Summarize the importance ...'
[2024-06-22 22:20:51] [SYMBOLIC-AI|RESULT] Symbolic backend result: [SYMBOLIC/LLM RESULT] Symbolic logic is foundational to ...
```

### Where to find logic and logs
- **API logic:** `symbolic_ai_service/backend/symbolic_service.py`
- **Backend agent:** `backend_core_service/backend/core/autonomous_agent.py`
- **Logs:** `symbolic_ai_service/logs/symbolic_reasoning.log`

### Why
- Ensures all symbolic/NLU workflows flow through a single explicit reasoning path and robustly use the same backend logic as all other autonomy/automation scenarios.
- All key events, errors, and results are logged for rapid support and analysis.

---
This now ensures all symbolic/test/NLU pathways in Sonny are robust, auditable, and aligned with production backend decision-making.