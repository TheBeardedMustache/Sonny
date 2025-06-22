# Sonny Long‑Term Stability & Stress Testing

This document outlines procedures for extended stability and stress testing to ensure Sonny remains robust under continuous load.

## 1. Locust Stress Tests

Use the `locustfile.py` for multi‑endpoint load scenarios:

```bash
# Run Locust against the Backend Core API
locust -f locustfile.py --host=http://localhost:${BACKEND_PORT}
```

- **Start with low users**: `-u 10 -r 2`
- **Ramp up**: increase to `-u 100 -r 10` over a 30-minute window
- **Run**: soak the system for 1+ hour

## 2. Observability During Stress

- Monitor Prometheus/Grafana dashboards for CPU, memory, latency spikes
- Watch container health (`docker-compose ps`) to detect restarts or failures

## 3. Resource Saturation Tests

- Simulate out‑of‑memory or CPU starved conditions (e.g., Cgroups limits)
- Verify graceful degradation and auto‑recovery via healthchecks and restart policies

## 4. Regression Verification

- Post‑stress, re‑run unit/integration tests to confirm no regressions:
  ```bash
  pytest -q --disable-warnings
  ```

## 5. Reporting

- Capture stress test metrics (requests/sec, error rates, p95 latency)
- Document in a summary report with graphs/screenshots

## 6. Next Steps

- Automate stress runs in CI pipeline for nightly builds
- Integrate SLO/SLI thresholds for automated alerts