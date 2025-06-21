import time
import pytest

# Flask proxies exposing healthz and metrics
from services.frontend_service.frontend_flask import app as frontend_app
from services.backend_core_service.backend_core_flask import app as backend_app
from services.symbolic_ai_service.symbolic_ai_flask import app as symbolic_app


@pytest.mark.parametrize("app,health_path", [
    (frontend_app, "/healthz"),
    (backend_app, "/healthz"),
    (symbolic_app, "/healthz"),
])
def test_healthz_endpoint(app, health_path):
    client = app.test_client()
    for _ in range(3):
        start = time.time()
        resp = client.get(health_path)
        latency = time.time() - start
        assert resp.status_code == 200
        assert resp.get_json() == {"status": "ok"}
        assert latency < 0.2


@pytest.mark.parametrize("app", [frontend_app, backend_app, symbolic_app])
def test_metrics_endpoint(app):
    client = app.test_client()
    resp = client.get("/metrics")
    assert resp.status_code == 200
    # Prometheus metrics should be plain text
    assert "text/plain" in resp.content_type