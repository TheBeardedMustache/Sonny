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
from flask import Flask, request, Response
import requests
from flask_talisman import Talisman
from pythonjsonlogger import jsonlogger

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

app = Flask(__name__)
# Security: enforce HTTPS & default security headers
Talisman(app, force_https=True)

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

@app.route('/healthz', methods=['GET'])
def healthz():
    """Health check endpoint."""
    return {'status': 'ok'}

if __name__ == "__main__":
    # Launch the FastAPI core service in background, then start Flask proxy
    thread = threading.Thread(target=run_fastapi, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=FLASK_PORT)