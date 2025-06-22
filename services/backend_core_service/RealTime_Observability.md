Real-Time Observability: Logging, Prometheus, Grafana
====================================================

This document summarizes how unified logs and metrics are made available for real-time observability and monitoring for Sonny.

## Streamlit Real-Time Log Monitoring
- **Frontend chat UI** displays: backend autonomy logs, symbolic AI logs, error handling logs, and frontend chat logs in real time.
    - Columns for [Frontend], [Backend], [Symbolic AI], and [Errors] present the most recent tail.
- Users can instantly see backend errors, step-by-step autonomy decisions, symbolic interpretations, and chat messages for every operation.
- The "Refresh All Logs" button triggers an immediate UI refresh, supporting continuous monitoring in mission control/use.

## Prometheus & Grafana Integration
- Prometheus scrapes `/metrics` endpoints for backend and symbolic AI by default (see prometheus.yml).
- Compose service for `grafana` is present for rapid dashboarding.
- **Recommended Grafana dashboards:**
    - Log rate/level panels (using promtail or Loki for easy log ingestion)
    - Error/exception counters by log file (backend Errors, Symbolic Errors)
    - Service health indicators tracked via metrics endpoints
    - Custom panels for symbolic/decision outcomes classified by Silver/Gold/Cinnabar path

### Example Prometheus scrape job:
```
  - job_name: 'backend_core_service'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['backend_core_service:8000']
```
---
With these patterns, you gain real-time observability of system health, low-level code reasoning, symbolic outcomes, and all error events.