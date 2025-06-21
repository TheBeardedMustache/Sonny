## Backend Core Service

**Purpose**: Expose Sonny’s core symbolic reasoning and automation logic via FastAPI.

### Components
- FastAPI app defined in `backend/api.py`, with endpoints:
  - `/process/` for full request processing.
  - Root `/` for health check.
- Environment loading and logging in `backend/api.py`.
- Core logic resides in `backend/core/` and `backend/cinnabar/` modules.

### Docker Packaging
- Uses `Dockerfile.backend` at project root.
- Exposes port `8000`.
- CMD: `uvicorn backend.api:app --host 0.0.0.0 --port 8000`

### Deployment
1. Build image: `docker build -f Dockerfile.backend -t sonny-backend .`
2. Run container: `docker run -d -p 8000:8000 --env-file .env sonny-backend`

### Testing
- Ensure `pytest tests/test_core* tests/test_cinnabar*` passes.