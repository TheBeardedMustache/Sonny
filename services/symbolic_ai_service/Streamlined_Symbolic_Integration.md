## Streamlined Symbolic Integration

### Overview
The NLU pipeline and symbolic reasoning endpoints have been simplified and made explicit. Every major symbolic reasoning step and LLM output is logged to a central file for tracing, robustness, and debugging.

### Key Changes
- **NLU (`interpret_input`)** is now clearly streamlined:
    - Validates input robustly, logs input and validation outcome
    - All OpenAI LLM outputs and errors are logged with clear context
    - Symbolic state changes and result content are logged with timestamps
- **API Endpoint `/interpret/`**:
    - Logs calls, outcomes, and errors in `logs/symbolic_reasoning.log`
    - Robustly propagates any error, with logging for both input and error details
- **All symbolic steps are now visible** in `logs/symbolic_reasoning.log` for each request.

### Log File Location
- `services/symbolic_ai_service/logs/symbolic_reasoning.log` (timestamped, plaintext)

**Log Example:**
```
[2024-06-22 18:44:18] API /interpret/ called with: 'list my calendar events'
[2024-06-22 18:44:18] interpret_input received: 'list my calendar events' [model=gpt-4, max_tokens=256]
[2024-06-22 18:44:18] Valid input accepted: 'list my calendar events'
[2024-06-22 18:44:21] LLM output for 'list my calendar events': intent: list_calendar_events...
[2024-06-22 18:44:21] Symbolic state updated. Output: intent: list_calendar_events...
[2024-06-22 18:44:21] interpret_input result: intent: list_calendar_events...
```

### Enhanced Robustness & Accuracy
- If input is empty or invalid, this is explicitly logged and a detailed error returned.
- All reasoning, interpretation steps, model outputs, and errors are logged out of band for auditability and troubleshooting.

---
**Endpoints affected:** `/interpret/` (NLU intent detection)  
**Source logic:** `backend/cinnabar/nlu.py`, `backend/symbolic_service.py`