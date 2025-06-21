## Symbolic AI & Codex Service

**Purpose**: Provide dedicated microservice for symbolic reasoning and Codex API interactions.

### Components
- FastAPI app defined in `backend/symbolic_service.py`, exposing endpoints:
  - `/interpret/` for NLU interpretation.
  - `/respond/` for assistant response generation.
  - `/script/` for Python script generation.
- Utilizes modules in `backend/cinnabar/` and `backend/core/codex_auto.py`.

### Docker Packaging
- Uses `Dockerfile.symbolic` at project root.
- Exposes port `9000`.
- CMD: `uvicorn backend.symbolic_service:app --host 0.0.0.0 --port 9000`

### Deployment
1. Build image: `docker build -f Dockerfile.symbolic -t sonny-symbolic .`
2. Run container: `docker run -d -p 9000:9000 --env-file .env sonny-symbolic`

### Testing
- Ensure `pytest tests/test_cinnabar* tests/test_core*` passes, focusing on symbolic endpoints.