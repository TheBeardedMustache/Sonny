## Frontend Service

**Purpose**: Provide interactive Streamlit UI for Sonny's automation paths.

### Components
- Codebase under `frontend/` directory.
- Entry point: `frontend/app.py` with component routing.
- UI modules: `frontend/components/*.py` for Home, Silver, Gold, Cinnabar, Combined.

### Docker Packaging
- Uses `Dockerfile.frontend` at project root.
- Exposes port `8501`.
- CMD: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.enableCORS=false`

### Deployment
1. Build image: `docker build -f Dockerfile.frontend -t sonny-frontend .`
2. Run container: `docker run -d -p 8501:8501 --env-file .env sonny-frontend`

## Environment Variables

- `BACKEND_CORE_URL` (default: http://backend_core_service:8000): Base URL for the Backend Core API.

### Testing
- Ensure `pytest tests/test_frontend*.py` passes.