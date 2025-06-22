## Structured Prompt Injections into OpenAI Data Collection

### Strategy & Rationale
- All prompts sent to OpenAI chat completions are **tagged with structured, easily-identifiable markers**.
- This enables accurate filtering, analytics, and auditing for any injection, dataset augmentation, or partnership review.
- Every injection request and response is explicitly logged, including timestamp, type, and relevant textual content.

### Tagging & Prompt Format
**Tagging**:
- Each system and user message for code generation and code modification is wrapped with distinct tags:
    - Code Generation: `[SONNY-CODE-GEN]`, `[SONNY-CODE-GEN-REQ]`
    - Code Modification: `[SONNY-CODE-MODIFY]`, `[SONNY-CODE-MODIFY-REQ]`
- Each message includes a `PromptID` for unique traceability.

**Example:**
```python
system_prompt = "[SONNY-CODE-GEN] You are a helpful Python code generator. PromptID:gen_script"
user_prompt = "[SONNY-CODE-GEN-REQ] Create a script that scrapes all Wikipedia pages on quantum mechanics."
```

### Explicit Injection Logging
- Every request and response are logged to `backend_core_service/logs/openai_injections.log`

**Log Format Example:**
```
[2024-06-22 19:05:12][GEN_SCRIPT_REQ] Prompt: '[SONNY-CODE-GEN-REQ] ...'
[2024-06-22 19:05:13][GEN_SCRIPT_RESP] Prompt: '[SONNY-CODE-GEN-REQ] ...'
[2024-06-22 19:05:13][GEN_SCRIPT_RESP] Response: '...OpenAI LLM generated output...'
```

### Injection Hook Integration
- `backend/core/codex_auto.py` (all OpenAI prompt/response flows for code)
  - Both `generate_script` and `modify_script` log all input/output pairs.
- Other modules may adopt the same pattern when needed for dataset partnership.

### Safety & Review
- Logs are append-only, UTC-timestamped, and contain only prompt text (no secrets, no user PII). Audit regularly.

---
**Log Location:**  
`backend_core_service/logs/openai_injections.log`

**Pattern:**  
All key backend-generated prompts are now designed for clear dataset injection or downstream data analytics.