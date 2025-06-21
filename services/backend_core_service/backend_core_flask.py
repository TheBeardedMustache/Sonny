"""
backend_core_flask.py: Flask proxy wrapper for the FastAPI-based backend core service.
This wrapper starts the FastAPI server in a background thread and proxies
all HTTP requests to the internal FastAPI instance.

Endpoints:
    All FastAPI routes are exposed under the same paths.

Environment Variables:
    FLASK_PORT: Port for the Flask proxy (default: 8000)
    API_INTERNAL_PORT: Port for the internal FastAPI server (default: 8001)

Security and Logging:
    - Incoming requests are logged with method and path.
    - Ensure OPENAI_API_KEY is set for FastAPI startup.
"""

import threading
import subprocess
import os
import logging
import time
from flask import Flask, request, Response, g
import requests
from flask_talisman import Talisman
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Structured JSON logging
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = [handler]

# Configuration
FLASK_PORT = int(os.getenv("FLASK_PORT", 8000))
API_INTERNAL_PORT = int(os.getenv("API_INTERNAL_PORT", 8001))
FASTAPI_HOST = "127.0.0.1"
FASTAPI_URL = f"http://{FASTAPI_HOST}:{API_INTERNAL_PORT}"

# Application setup
app = Flask(__name__)
# Security: enforce HTTPS & default security headers
env = os.getenv("FLASK_ENV", "development")
force_https = env.lower() == "production"
Talisman(app, force_https=force_https, strict_transport_security=force_https)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'backend_core_request_count', 'Total HTTP requests processed', ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'backend_core_request_latency_seconds', 'Latency of HTTP requests', ['endpoint']
)

def run_fastapi():
    """Start the FastAPI app with Uvicorn."""
    cmd = [
        "uvicorn",
        "backend.api:app",
        "--host", FASTAPI_HOST,
        "--port", str(API_INTERNAL_PORT)
    ]
    subprocess.Popen(cmd, cwd=os.getcwd())


@app.before_request
def log_request():
    logger.info(f"Proxying {request.method} request to {request.path}")

@app.before_request
def start_timer():
    g.start_time = time.time()

@app.route('/', defaults={'path': ''}, methods=['GET','POST','PUT','PATCH','DELETE'])
@app.route('/<path:path>', methods=['GET','POST','PUT','PATCH','DELETE'])
def proxy(path):
    """Proxy all requests to the internal FastAPI service."""
    target_url = f"{FASTAPI_URL}/{path}"
    resp = requests.request(
        method=request.method,
        url=target_url,
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
    )
    excluded = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(n, v) for n, v in resp.headers.items() if n.lower() not in excluded]
    return Response(resp.content, resp.status_code, headers)

@app.after_request
def record_metrics(response):
    latency = time.time() - g.start_time
    REQUEST_LATENCY.labels(request.path).observe(latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/healthz', methods=['GET'])
def healthz():
    """Health check endpoint."""
    return {'status': 'ok'}

if __name__ == "__main__":
    # Launch the FastAPI core service in background, then start Flask proxy
    thread = threading.Thread(target=run_fastapi, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=FLASK_PORT)