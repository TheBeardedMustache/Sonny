# Symbolic AI Service API

The Flask proxy for the Symbolic AI FastAPI microservice exposes LLM-powered endpoints and a health check on port 8001.

| Endpoint      | Method(s) | Description                                |
|---------------|-----------|--------------------------------------------|
| `/healthz`    | GET       | Returns service health status.             |
| `/interpret/` | POST      | Parse text to high-level intent.           |
| `/respond/`   | POST      | Generate assistant response text.          |
| `/script/`    | POST      | Generate Python script from prompt.        |
| `/`           | GET,POST,PUT,PATCH,DELETE | Reverse-proxies to FastAPI docs/root. |

## Common request format
All LLM endpoints accept JSON payloads:
```json
{ "text": "your input text or prompt" }
```

## Sample Responses
- **/interpret/**: `{ "intent": {...} }`
- **/respond/**  : `{ "response": "assistant reply" }`
- **/script/**   : `{ "code": "def foo(): ..." }`