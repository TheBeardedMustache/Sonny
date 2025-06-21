# Backend Core Advanced Optimization

This guide describes performance enhancements to improve throughput and reduce latency in the Backend Core microservice.

## 1. Asynchronous Proxying with httpx

- Replace blocking `requests` calls with `httpx.AsyncClient` in `/interpret/`, `/respond/`, and `/script/` endpoints for non-blocking I/O.

## 2. GZip Compression

- Use FastAPI's `GZipMiddleware` to compress responses over a size threshold:

```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=500)
```

## 3. Worker Process Scaling

- In production, run Uvicorn with multiple workers:

```bash
uvicorn backend.api:app --host 0.0.0.0 --port 8000 --workers 4
```

## 4. Pydantic Tuning

- Configure `BaseModel.Config` options to reduce validation overhead on high-frequency endpoints.

```python
class TextRequest(BaseModel):
    text: str
    class Config:
        validate_assignment = False
        arbitrary_types_allowed = True
```

## 5. Future Caching Strategies

- Integrate a distributed cache (e.g., Redis via `fastapi-cache2`) for idempotent or expensive responses.

## 6. Lightweight Health Checks

- Ensure `/healthz` does minimal work (no imports of heavy modules) to quickly respond and avoid timeout failures.