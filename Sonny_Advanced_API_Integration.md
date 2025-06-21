# Sonny Advanced API Integration

This guide describes how the Frontend, Backend Core, and Symbolic AI microservices interact via explicit REST APIs.

## Services & Endpoints

| Service                | URL (Docker Compose)             | Description                     |
|------------------------|----------------------------------|---------------------------------|
| Frontend Service       | http://frontend_service:8501     | Streamlit UI via Flask proxy    |
| Backend Core Service   | http://backend_core_service:8000 | Core API via Flask proxy        |
| Symbolic AI Service    | http://symbolic_ai_service:8001  | Symbolic AI API via Flask proxy |

### 1. Frontend → Backend Core

#### Process User Input
- **POST** `/process/`
- **Request**: `{"text": "<user text>"}`
- **Response**: `{"response": "<LLM response>"}`

#### Fetch Symbolic State
- **GET** `/state/`
- **Response**: Current symbolic state as JSON

#### Interpret (Proxied)
- **POST** `/interpret/`
- **Request**: `{"text": "<user text>"}`
- **Response**: `{"intent": "<intent>"}`

#### Respond (Proxied)
- **POST** `/respond/`
- **Request**: `{"text": "<user text>"}`
- **Response**: `{"response": "<assistant response>"}`

#### Generate Script (Proxied)
- **POST** `/script/`
- **Request**: `{"prompt": "<script prompt>"}`
- **Response**: `{"code": "<python code>"}`

##### Example (Python)
```python
import os, requests

BASE = os.getenv("BACKEND_CORE_URL", "http://localhost:8000")

# Process
r = requests.post(f"{BASE}/process/", json={"text": "Hello Sonny"})
print(r.json())

# Fetch state
r = requests.get(f"{BASE}/state/")
print(r.json())
```

## 2. Backend Core → Symbolic AI

The Backend Core service proxies to the Symbolic AI service according to the `$SYMBOLIC_AI_URL` environment variable (default: `http://127.0.0.1:8001`).

Endpoints are forwarded verbatim:
- **POST** `/interpret/`
- **POST** `/respond/`
- **POST** `/script/`

## 3. Symbolic AI Service

Implemented in `symbolic_service.py` using Pydantic models for JSON I/O:

```jsonc
POST /interpret/  { "text": "<input>" }   -> { "intent": "<intent>" }
POST /respond/    { "text": "<input>" }   -> { "response": "<answer>" }
POST /script/     { "prompt": "<input>" } -> { "code": "<python code>" }
```

All endpoints use JSON request/response schemas.

## Configuration

- **Frontend**: `BACKEND_CORE_URL` (default `http://backend_core_service:8000`)
- **Backend Core**: `SYMBOLIC_AI_URL` (default `http://symbolic_ai_service:8001`)

Ensure these are set in your environment or in `docker-compose.yml`.