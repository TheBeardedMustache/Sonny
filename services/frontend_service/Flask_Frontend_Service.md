# Flask Frontend Service

This service wraps the Streamlit UI in a minimal Flask application. It provides a single entry point for all frontend requests.

## Endpoints

| Path       | Method | Description                                         |
|------------|--------|-----------------------------------------------------|
| /<path>    | GET    | Redirects to the Streamlit UI at the same path.     |
| /          | GET    | Redirects to the home page of the Streamlit app.    |

## Environment Variables

- `FLASK_PORT` (default: 8501): Port on which the Flask server listens.
- `STREAMLIT_PORT` (default: 8502): Port on which the Streamlit server listens.

## Security

- All traffic is proxied via the Flask server.
- Consider adding authentication, HTTPS termination, and CORS policies for production.

## Usage

```bash
FLASK_PORT=8501 STREAMLIT_PORT=8502 python frontend_flask.py
```