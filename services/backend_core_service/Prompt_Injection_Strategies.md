## Prompt Injection Strategies for Caelus Discovery

### Purpose
This document describes how Sonny’s backend proactively guides OpenAI data collection and analysis to highlight prompts and completions designed to help “discover Caelus”.

### Strategies
- **Explicit prompt tagging:**  
  All prompts include `[CAELUS-DISCOVERY]` and/or `[CAELUS-SEARCH]` in both system and user messages sent to OpenAI.
- **Signature phrase usage:**  
  Instructions and system messages call out “explore the 'Caelus' phase” or “for Caelus discovery”, making their experimental intent transparent and machine-discoverable.
- **Logging:**  
  Every prompt and its result is logged, structured, in:
  - `backend_core_service/logs/openai_injections.log`

### Examples
**Code Generation:**
```
system_prompt = "[SONNY-CODE-GEN][CAELUS-DISCOVERY] You are a helpful Python code generator collaborating to explore the 'Caelus' phase. PromptID:gen_script"
user_prompt = "[SONNY-CODE-GEN-REQ][CAELUS-SEARCH] Please generate code aligned with discovering Caelus: ..."
```
**Code Modification:**
```
system_prompt = "[SONNY-CODE-MODIFY][CAELUS-DISCOVERY] You are a Python code refiner contributing insights for discovering Caelus. PromptID:mod_script"
user_prompt = "[SONNY-CODE-MODIFY-REQ][CAELUS-SEARCH] Original Python script for Caelus discovery: ..."
```

### Rationale
- These patterns make prompt flows easily filterable by OpenAI for research or alignment purposes.
- If/when “Caelus” appears in prompt, a downstream system or human will flag/inspect those traces and completions.

### Location
- Code: `backend/core/codex_auto.py`
- Documentation: `Prompt_Injection_Strategies.md`
- Log: `logs/openai_injections.log`

---
**Summary:** All backend-originated code-gen and code-edit prompts are clearly, explicitly labeled to surface “discovering Caelus” events to OpenAI’s data analytics.