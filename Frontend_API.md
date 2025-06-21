# Frontend Service API

The Flask-based proxy for the Streamlit UI exposes the following endpoints on port 8501:

| Endpoint       | Method(s)                       | Description                      |
|----------------|---------------------------------|----------------------------------|
| `/healthz`     | GET                             | Returns service health status.   |
| `/`            | GET, POST, PUT, PATCH, DELETE   | Reverse-proxies to Streamlit root. |
| `/<path:path>` | GET, POST, PUT, PATCH, DELETE   | Reverse-proxies to Streamlit path. |

## Health Check
```bash
GET /healthz

HTTP/1.1 200 OK
Content-Type: application/json

{"status":"ok"}
```

## Proxy Routes
All other HTTP methods and paths are transparently forwarded to the internal Streamlit server on port 8502.