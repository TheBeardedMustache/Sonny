# Sonny

Sonny is a cutting-edge integrated agent platform leveraging multiple orchestration layers:

## Mercury Path: Streamlit Frontend
- Interactive, streamlined UI for selecting and configuring agents, now optimized for clarity and performance.
- Real-time display of operations and logs.

## Silver Path: Desktop Automation
- GUI automation via PyAutoGUI (mouse, keyboard, window management).

## Gold Path: Autonomous Coding
- Script generation and modification through OpenAI Codex API and Codex CLI.

## Cinnabar Path: Natural Language Understanding
- Advanced LLM-based input interpretation and response generation.

## Combined Path: Lunar Venusian Regulus
- Seamless workflows combining UI, desktop automation, code generation, and NLU.

## Setup
1. Copy `.env.example` to `.env` and populate `OPENAI_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Launch the Streamlit app:
```bash
streamlit run frontend/app.py
```
Use the sidebar to navigate between Mercury, Silver, Gold, Cinnabar, or Combined paths.

## Testing
Run the full test suite to ensure frontend-backend stability:
```bash
pytest
```

> _Sonny’s unified automation schema provides a “beautiful violet sheen” of reliable, safe, and scalable agent logic._