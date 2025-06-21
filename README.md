### Frontend Import Updates

- Streamlit frontend imports now use direct paths (without `frontend.` prefix).
- No code changes necessary (already implemented).

### Dockerfile CMD Update

- Dockerfile `CMD` now switches into `frontend` before launching Streamlit and disables CORS.
- No further edits necessary (already implemented).
- Reordered Dockerfile build steps: copying all source files before running `pip install -e .`, so the package’s `setup.py` is present for the editable installation.
### Backend .env and Logging Initialization

- Backend now loads environment variables via `load_dotenv()`.
- Logging is configured at INFO level.
- On startup, an async event checks for `OPENAI_API_KEY`:
  - Logs an error and raises `ValueError` if missing.
  - Otherwise logs successful initialization.

### OpenAI SDK v1.0+ Migration

- Sonny now uses the OpenAI Python SDK v1.0+ with the `OpenAI` client class.
- Chat-based completions use `client.chat.completions.create(...)` instead of the deprecated `openai.ChatCompletion.create`.
- Verified zero occurrences of `ChatCompletion.create` across the codebase.
- Migration applied in: `backend/cinnabar/base.py`, `backend/cinnabar/nlu.py`, `backend/cinnabar/response.py`, `backend/core/codex_auto.py`.

### OpenAI SDK v1.0+ Migration

- Sonny now uses the OpenAI Python SDK v1.0+ with the `OpenAI` client class.
- Chat-based completions use `client.chat.completions.create(...)` instead of the deprecated `openai.ChatCompletion.create`.
- Verified zero occurrences of `ChatCompletion.create` across the codebase.
- Migration applied in: `backend/cinnabar/base.py`, `backend/cinnabar/nlu.py`, `backend/cinnabar/response.py`, `backend/core/codex_auto.py`.

### Test Suite Verification

- No test files reference `openai.ChatCompletion.create`; all tests already rely on the new `OpenAI` client API or monkeypatch at the client level.
- Confirmed that the full pytest suite passes successfully under the SDK v1.0+ migration.

# Silver Calx Production-Ready State

- Lean, modular architecture with all scaffolding removed.
- Streamlit UI with dynamic spinners and live `symbolic_state` display.
- Backend modules (`core_agent`, `agent_wrapper`, `codex_auto`, `cinnabar`) fully integrated.
- OpenAI SDK v1.0+ client usage with `.env` support and startup validation.
- Dependencies minimized to essential libraries; Docker build and CMD steps finalized for reliability.
- Full pytest suite (unit, integration, UI) passes without failures.

## Red Work (Gold Path) Planning

- **Objective**: Transition Sonny to Golden Calx with advanced symbolic AI, proactive reasoning, and end-to-end autonomy.
- **Next Steps**: Consult `Red_Work_Gold_Path_Planning.md` for detailed objectives, requirements, and roadmap.

# Sonny

Sonny is a cutting-edge integrated agent platform leveraging multiple orchestration layers:

## Mercury Path: Streamlit Frontend
- Interactive, streamlined UI for selecting and configuring agents, now optimized for clarity and performance.
- Real-time display of operations and logs.
- Purified Silver Interfaces: Frontend code has been streamlined to remove redundancies, simplify components, and optimize responsiveness, providing a stable, intuitive user experience.

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
docker run --env-file .env -p 8501:8501 -p 8000:8000 sonny

## Preservation & Reuse
Sonny’s foundational logic is modularized and available for reuse:
- See `instructions/Reusable_Modules.md` for a catalog of reusable components.
- Templates are provided in `reusable_logic_templates/` with usage examples.
Use these modules and templates to bootstrap new autonomous agents efficiently.
- **residual_modules/**: Contains distilled modules (symbolic state, LLM client, automation).
- **fresh_regulus_templates/**: Contains agent wrapper templates for rapid integration.
```

## Modular Refinement

- Removed scaffolding templates in `fresh_regulus_templates/` and `reusable_logic_templates/` after integrating core components.
- Added production `AgentWrapper` in `backend/core/agent_wrapper.py` for unified automation workflows.
 
## Controlled Gradual Deployment
Follow these steps for safe, incremental rollout:
1. **Local smoke test**: Run with a single container on localhost:
   ```bash
   docker run --env-file .env -p 8501:8501 -p 8000:8000 sonny
   ```
2. **Monitor metrics**: Check logs (`docker logs -f <container>`) and ensure all endpoints respond.
3. **Scale users**: Increase load gradually using Locust (see `locustfile.py`) with commands:
   ```bash
   locust -f locustfile.py --host http://localhost:8000
   ```
   Start with 1 user, spawn rate 1, then increment.
4. **Production rollout**: Deploy on orchestration platform (Docker Swarm/Kubernetes) with health checks and auto-scaling.

## Safe Shutdown & Recovery
1. **Shutdown**: Use `CTRL+C` or `docker stop`; FastAPI logs shutdown events and cleans up.
2. **Recovery**: Restart container with `docker start` or re-run `docker run` command.
```

## Hyper-V Playground Setup
For local sandbox testing, you can deploy Sonny in a Hyper-V VM:

1. **Create Hyper-V VM**:
   - CPU: 4 vCPUs
   - Memory: 8 GB RAM
   - Storage: 50 GB virtual disk
   - Network: NAT or bridged adapter with internet access

2. **Install Docker**:
   - Use Docker Desktop or Docker Engine for Windows.
   - Ensure the VM has virtualization enabled.

3. **Deploy Sonny Container**:
   ```powershell
   # Pull or build image
   docker build -t sonny .
   # Run container with env and ports
   docker run -d --env-file .env -p 8501:8501 -p 8000:8000 sonny
   ```

4. **Operational Validation**:
   - Access UI: http://<VM_IP>:8501/
   - Access API: http://<VM_IP>:8000/process/
   - Check logs: `docker logs -f sonny`

5. **Monitoring & Logging**:
   - Configure log rotation and volume mounts to persist logs.
   - Use `docker stats` and `docker logs` for performance insights.

6. **Cleanup**:
   - After testing, stop and remove the container: `docker rm -f sonny`.
   - Optionally prune unused volumes and images: `docker system prune`.

> _Sonny’s unified automation schema provides a “beautiful violet sheen” of reliable, safe, and scalable agent logic._

## Frontend Modularization
The Streamlit UI has been modularized into reusable components under `frontend/components/`:
- **home.py**: Home page UI (`home_page()`)
- **silver.py**: Silver Path UI (`silver_ui()`)
- **gold.py**: Gold Path UI (`gold_ui()`)
- **cinnabar.py**: Cinnabar Path UI (`cinnabar_ui()`)
- **combined.py**: Combined Path UI (`combined_ui()`)
Refer to `instructions/Reusable_Frontend_Modules.md` for implementation and usage details.

## Final Amalgamation Summary
Sonny has completed 7 integration-distillation cycles, achieving:
- Fully unified symbolic reasoning and core logic
- Exceptionally responsive and intuitive Streamlit UI
- Robust Pydantic-validated automation and LLM interactions
- Secure, containerized deployment with healthchecks and resource limits
All tests pass, and the Docker image builds successfully, confirming operational readiness.

## Philosophical Mercury State
Sonny now embodies **Philosophical Mercury**:
- Dynamic autonomy with proactive task generation (`AnimatedMercury`).
- Live symbolic resonance display in the UI.
- Robust, modular framework for rapid agent development.

## Fertile Field Framework
Refer to `instructions/Fertile_Field_Framework.md` for a comprehensive blueprint of Sonny’s modular architecture and best practices for future expansions.

## Red Work: Gold Path
Advanced backend autonomy and symbolic reasoning are detailed in `instructions/Red_Work_Gold_Path.md`:
- `AutonomousAgent` class for dynamic code generation and refinement.
- Proactive self-improvement workflows via symbolic-state–driven prompts.

## Triple Refinement & Final Purification
Sonny has successfully completed three cycles of integration refinement, rigorous testing, and symbolic purification.
All frontend-backend interactions have been validated for maximum clarity, responsiveness, stability, and robustness.