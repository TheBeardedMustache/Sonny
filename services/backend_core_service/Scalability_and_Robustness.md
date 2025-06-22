Scalability and Robustness
=========================

This document captures explicit strategies and configuration for horizontal scaling, error handling, and resource management in Sonny's architecture.

## Horizontal Scaling (Docker Compose)
- All major services (frontend, backend, symbolic) are horizontally scalable via `docker-compose.yml` with `deploy.replicas: 3` as a default. This can be tuned via environment variables.
- Load balancers, restart policies, and log rotation are configured for robust HA/fault-tolerance.
- Typical scaling scenario: simply increase `replicas` for the desired service, and containers will be orchestrated accordingly.

## Error Handling
- All exceptions in backend task selection and actions are logged to `logs/error_handling.log`.
- Each call to CMD, Codex, LLM, or other critical functions includes `try/except` logic, which logs recoverable and fatal errors.
- Recovery: Most user-facing flows catch exceptions and continue to serve partial results or error messages, maximizing resilience under load.
- Logfile rotation (`max-size`, `max-file`) in Docker Compose keeps logs from accreting without bound.

## Resource Management
- Each service in Docker Compose can specify `mem_limit`, `cpus`, and restart policies for service stability and predictability under contention.
- Healthchecks for both Streamlit and Flask/FastAPI ensure prompt restarts or rescheduling on node/container failure.
- Long-running subprocesses and external API calls should ideally use smart timeboxing and deadline controls (timeouts).
- For improved scaling or deployment robustness, consider:
    - Terminating idle or unhealthy containers automatically.
    - Running services under non-root, least-privilege Docker users.
    - Monitoring with Prometheus/Grafana (present in docker-compose).

## Example settings (excerpt from docker-compose.yml):

```
  backend_core_service:
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    # Optionally add
    mem_limit: 1g
    cpus: 0.5
    healthcheck:
      test: curl -f http://localhost:8000/healthz || exit 1
      interval: 30s
      timeout: 5s
      retries: 3
```