# Flask Symbolic AI Service

This Flask wrapper proxies requests to the FastAPI-based Symbolic AI microservice.

## Endpoints

| Path           | Method | Description                                      |
|----------------|--------|--------------------------------------------------|
| /interpret/    | POST   | Interpret user text to high-level intents.       |
| /respond/      | POST   | Generate assistant responses.                    |
| /script/       | POST   | Generate Python scripts from prompts.            |
| /              | Any    | Proxy route for health checks and root endpoints.|

The proxy supports GET, POST, PUT, PATCH, and DELETE for all routes.

## Environment Variables

- `FLASK_PORT` (default: 8001): Port on which Flask listens.
- `SYMBOLIC_INTERNAL_PORT` (default: 9000): Port for the internal FastAPI server.
- `OPENAI_API_KEY`: Required for LLM-based endpoints.

## Logging and Security

- Incoming requests are logged with method and path.
- Ensure `OPENAI_API_KEY` is secured and not logged.
- Consider adding authentication, rate limiting, and HTTPS for production.

## Usage

```bash
FLASK_PORT=8001 SYMBOLIC_INTERNAL_PORT=9000 OPENAI_API_KEY=your_key python symbolic_ai_flask.py
```