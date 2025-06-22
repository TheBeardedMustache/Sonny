# Sonny Final Monitoring

This document details the final continuous monitoring and dashboard setup for the fully mature Sonny platform, using Prometheus and Grafana.

## 1. Grafana Provisioning

Grafana is preconfigured via provisioning files under `monitoring/grafana/provisioning/`:

```bash
monitoring/grafana/
├── provisioning/
│   ├── datasources/
│   │   └── prometheus.yml
│   └── dashboards/
│       └── sonny_dashboards.yml
└── dashboards/
    └── sonny_overview.json
```

### 1.1 Data Source
`prometheus.yml` defines the Prometheus data source:
```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

### 1.2 Dashboards
`sonny_dashboards.yml` instructs Grafana to load JSON dashboards from `dashboards/`.

The key dashboard is `sonny_overview.json`, which contains:
- **Request Rate by Endpoint** (Frontend, Backend, Symbolic AI)
- **95th Percentile Latency** across all services

## 2. Accessing Grafana

After `docker-compose up`, access Grafana at `http://localhost:3000` (admin/admin). The “Sonny” folder will contain the provisioned dashboards.

## 3. Custom Dashboards

To extend or customize dashboards:
1. Edit or add JSON files under `monitoring/grafana/dashboards/`.
2. Update `sonny_dashboards.yml` if adding to a different folder or org.
3. Restart Grafana or wait for the provisioning interval.

## 4. Alerting & Notifications

Configure alert rules in Prometheus or Grafana UI for:
- High error rates (`rate(*_request_count_total[5m])`)
- Latency spikes (`histogram_quantile(0.95, *_request_latency_seconds_bucket)`)
- Container health (
  `probe_success{job="frontend_service"}`
)

## 5. Next Steps

- Integrate Slack/Email notifications for critical alerts.
- Automate dashboard updates via CI pipeline.