# Backend Core Service API

The Flask proxy for the FastAPI core service exposes all native FastAPI endpoints plus a health check on port 8000.

| Endpoint    | Method(s)                     | Description                            |
|-------------|-------------------------------|----------------------------------------|
| `/healthz`  | GET                           | Returns service health status.         |
| `/`         | GET, POST, PUT, PATCH, DELETE | Reverse-proxies to FastAPI root.       |
| `/process/` | POST                          | Process user text via symbolic logic.  |

## `/process/`
- **Request**
  - POST `/process/`
  - Content-Type: application/json
  - Body: `{ "text": "your input text" }`
- **Response**
  - 200 OK: `{ "response": "processed output" }`
  - 400 Bad Request on invalid input