# Flask Frontend Service

This service wraps the Streamlit UI in a minimal Flask application. It provides a single entry point for all frontend requests.

## Endpoints

| Path       | Method | Description                                         |
|------------|--------|-----------------------------------------------------|
| /<path>    | GET, POST, PUT, PATCH, DELETE | Proxies requests to the internal Streamlit server. |
| /          | GET, POST, PUT, PATCH, DELETE | Proxies requests to the root of the Streamlit app. |
| /healthz   | GET    | Health check endpoint, returns `{ 'status': 'ok' }`.     |

## Environment Variables

- `FLASK_PORT` (default: 8501): Port on which the Flask server listens.
- `STREAMLIT_PORT` (default: 8502): Port on which the Streamlit server listens.

## Security

- All traffic is proxied via the Flask server.
- Streamlit is launched with CORS disabled (`--server.enableCORS=false`) and XSRF protection disabled
  (`--server.enableXsrfProtection=false`) to avoid CORS/XSRF conflicts behind the proxy.
- Consider adding authentication, HTTPS termination, and stricter CORS policies for production.

## Usage

```bash
FLASK_PORT=8501 STREAMLIT_PORT=8502 python frontend_flask.py
```