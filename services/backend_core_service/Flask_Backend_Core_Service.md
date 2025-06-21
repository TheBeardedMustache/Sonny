# Flask Backend Core Service

This Flask wrapper proxies requests to the FastAPI-based backend core service, providing a single unified entry point.

## Endpoints

All FastAPI core endpoints are exposed via the same paths through this proxy:

| Path       | Method                 | Description                       |
|------------|------------------------|-----------------------------------|
| /          | GET                    | Healthcheck and root endpoints.   |
| /process/  | POST                   | Process text via symbolic logic.  |
| /healthz   | GET                    | Health check endpoint (status ok). |

The proxy supports GET, POST, PUT, PATCH, and DELETE for all routes.

| /healthz   | GET                    | Health check endpoint (status ok). |

## Environment Variables

- `FLASK_PORT` (default: 8000): Port on which Flask listens.
- `API_INTERNAL_PORT` (default: 8001): Port for the internal FastAPI server.
- `OPENAI_API_KEY`: Required for backend initialization.

## Logging

- Incoming HTTP requests are logged with method and path.
- FastAPI startup and shutdown events remain unchanged.

## Usage

```bash
FLASK_PORT=8000 API_INTERNAL_PORT=8001 OPENAI_API_KEY=your_key python backend_core_flask.py
```