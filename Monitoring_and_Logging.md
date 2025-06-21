# Monitoring and Logging Configuration

This document describes the structured logging and Docker Compose log settings for the Sonny Flask services.

## Structured JSON Logging
All Flask applications (frontend, backend core, symbolic AI) emit JSON-formatted logs for easy ingestion:

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

## Docker Compose Logging
The `docker-compose.yml` configures each service to use the `json-file` driver with rotation:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Container Healthchecks
Each service Dockerfile includes a `HEALTHCHECK` to detect failures and trigger restarts:

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:<port>/healthz || exit 1
```

## Viewing Logs
Use Docker Compose to follow logs for all services:

```bash
docker-compose logs -f
```

For production, integrate with centralized monitoring tools such as Prometheus (metrics), ELK (logs), and Grafana (dashboards).