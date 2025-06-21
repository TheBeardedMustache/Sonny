# Sonny Security Configuration

This document outlines the security measures applied to the Flask-encapsulated microservices in the Sonny project.

## Flask-Talisman (HTTPS & Security Headers)
Each Flask application (`frontend_flask.py`, `backend_core_flask.py`, `symbolic_ai_flask.py`) is wrapped with Flask-Talisman to enforce HTTPS and default security headers:

```python
from flask_talisman import Talisman
app = Flask(__name__)
Talisman(app, force_https=True)
```

This automatically configures headers including:
- `Strict-Transport-Security`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: deny`
- `X-XSS-Protection: 1; mode=block`
- Default Content Security Policy

## CORS & XSRF for Streamlit
Streamlit is launched behind the Flask proxy with CORS and XSRF disabled to avoid cross-origin conflicts:
```bash
streamlit run frontend/app.py \
  --server.enableCORS false \
  --server.enableXsrfProtection false
```
In production, consider enabling CORS with a restrictive policy and re-enabling XSRF protection.

## Structured JSON Logging
All services use JSON-formatted structured logging via `python-json-logger`:

```python
from pythonjsonlogger import jsonlogger
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = [handler]
```

## Container Hardening
- **Base images**: `python:3.11-slim` minimizes attack surface.
- **Healthchecks** ensure automated failover on container faults.
- **Log rotation** via Docker Compose limits disk usage.

## Recommendations
- Use a reverse proxy (e.g., NGINX, Traefik) with valid TLS certificates.
- Manage `OPENAI_API_KEY` via secrets vaults.
- Apply rate limiting and authentication (JWT, OAuth2) in production.