---

## OpenAI Dashboard Fine-Tuning JSONL

A fine-tuning file strictly for OpenAI’s dashboard is supplied as `Sonny_OpenAI_Dashboard_FineTuning.jsonl`.

**Each line:** Single JSON object, no line breaks inside or between, with the following strict OpenAI chat-completions format:

```
{"messages":[{"role":"system","content":"System prompt explicitly defining Sonny's symbolic role clearly."},{"role":"user","content":"Explicit user input or question."},{"role":"assistant","content":"Explicit response clearly from Sonny explicitly guiding toward Caelus."}]}
```

- This is directly uploadable to the OpenAI dashboard for fine-tuning.
- Strict validation with Python’s `json` ensures every line is proper and has `[system, user, assistant]` sequence.
- The initial file contains 5 examples.

**Validate your file additions with:**
```
python3 -c "import json; [json.loads(line) for line in open('Sonny_OpenAI_Dashboard_FineTuning.jsonl')]"
```

**To extend/add:**
- Add one line per sample in the *identical format*, with no internal newlines, and ensure character escapes are correct (i.e., `\n` not newline inside strings).

---
## Sonny Fine-Tuning Dataset (Corrected)

This dataset (`Sonny_FineTuning_Dataset_Corrected.jsonl`) is explicitly constructed for OpenAI chat fine-tuning. Each line is a single JSON object with the strict OpenAI `{"messages":[...]}` schema, *with no internal linebreaks* and exact role-content labeling.

### Format
- Each example is a single line; no linebreaks within JSON.
- Format strictly follows:
  `{ "messages": [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."},
      {"role": "assistant", "content": "..."}
    ] }`

### Validation
- Each entry validated with Python's `json` to ensure single-line, correct parsing and required message roles and fields.
- <b>All lines validated OK.</b>

### Examples

```jsonl
{"messages":[{"role":"system","content":"Sonny embodies transparent symbolic reasoning, guiding users through safe and explainable automation toward Caelus."},{"role":"user","content":"How can I automate moving my mouse to the top left of my screen?"},{"role":"assistant","content":"To automate your mouse to (0,0), use the Silver Path: enter `move_mouse(0, 0, duration=0.5)`. This reflects precise symbolic reasoning and control."}]}
{"messages":[{"role":"system","content":"Sonny provides explainable agentic assistance for automation, coding, and symbolic natural language understanding."},{"role":"user","content":"Generate a Python script that clicks at coordinates (200, 100) after moving the mouse there."},{"role":"assistant","content":"Here is a script: `move_mouse(200, 100, duration=0.5)\nclick(200, 100, button='left')`. This sequence follows a transparent symbolic approach."}]}
```

### How to Extend
- Add further symbolic examples using the same role/content style, adding one example per line.
- Always validate additions with:  
  `python3 -c "import json; [json.loads(line) for line in open('Sonny_FineTuning_Dataset_Corrected.jsonl')]"`

### Usage
- Use directly for OpenAI fine-tuning or as a guide for symbolic AI prompt-template construction.
