# Sonny Continuous Optimization

This guide describes how to set up continuous monitoring and iterative performance improvements using Prometheus and Grafana for Sonny's microservices.

## 1. Prometheus Setup

1. Ensure the `prometheus.yml` config file is present at the project root.
2. In `docker-compose.yml`, the `prometheus` service is defined:

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    ports:
      - "9090:9090"
    networks:
      - sonny_net
```

3. Prometheus will scrape the `/metrics` endpoint of each microservice every 15 seconds.

## 2. Grafana Setup

1. Grafana is defined in `docker-compose.yml`:

```yaml
  grafana:
    image: grafana/grafana:latest
    depends_on:
      - prometheus
    ports:
      - "3000:3000"
    networks:
      - sonny_net
```

2. Access Grafana at `http://localhost:3000` (default credentials: admin/admin).
3. Add Prometheus as a data source (`http://prometheus:9090`).

## 3. Instrumentation

Each Flask proxy service exposes a `/metrics` endpoint and tracks:
- **Request count** (`*_request_count` counter)
- **Request latency** (`*_request_latency_seconds` histogram)

For example, to view frontend metrics:
```bash
curl http://localhost:8501/metrics
```

## 4. Sample PromQL Queries

- Total backend_core requests per endpoint:
  ```promql
  sum by (endpoint) (backend_core_request_count_total)
  ```
- Average latency for symbolic_ai service:
  ```promql
  histogram_quantile(0.95, sum by (le) (symbolic_ai_request_latency_seconds_bucket))
  ```

## 5. Dashboard Ideas

- **Service overview**: Panel per service showing request rate and p95 latency.
- **Endpoint heatmap**: Heatmap of request counts over time grouped by endpoint.
- **Error rate**: Counter of non-2xx responses by service.

## 6. Iterative Optimization

1. Identify high-latency or high-error endpoints via Prometheus metrics.
2. Apply targeted optimizations (e.g., caching, async I/O).
3. Redeploy services and validate improvements via Grafana dashboards.
4. Repeat monitoring → optimization cycles regularly.