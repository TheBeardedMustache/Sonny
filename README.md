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

## Symbolic Resonance
Sonny tracks its symbolic reasoning via a **SymbolicState**:
- Records key events and their data for transparency.
- Exposed in the UI for real-time introspection and debugging.

This symbolic resonance ensures clear, trustworthy automation and reasoning.
## Structured Validation & Cleansing
Sonny integrates **Pydantic** models for robust input validation and data cleansing:
- **Coordinates & parameters**: Validates numeric ranges and types before automation actions.
- **Text & prompts**: Ensures non-empty strings and safe values for LLM interactions.
- **Error handling**: Logs validation failures and prevents invalid operations, preserving system stability.

## Setup
1. Copy `.env.example` to `.env` and populate `OPENAI_API_KEY`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## API Usage
Sonny exposes a FastAPI endpoint for symbolic reasoning:

### Start API Server
```bash
uvicorn backend.api:app --host 0.0.0.0 --port 8000
```

### Example Request
```bash
curl -X POST http://localhost:8000/process/ \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello"}'
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

## Docker Deployment
Build and run Sonny in a Docker container for secure, portable deployment:

```bash
# Build the Docker image
docker build -t sonny .

# Run the container (expose Streamlit port, load env vars)
docker run --env-file .env -p 8501:8501 sonny
```

> _Sonny’s unified automation schema provides a “beautiful violet sheen” of reliable, safe, and scalable agent logic._