"""
symbolic_ai_flask.py: Flask proxy wrapper for the FastAPI-based Symbolic AI service.
This wrapper starts the Symbolic AI FastAPI service in a background thread and proxies
all HTTP requests to the internal FastAPI instance.

Endpoints:
    All /interpret/, /respond/, and /script/ routes are exposed via this proxy.

Environment Variables:
    FLASK_PORT: Port for the Flask proxy (default: 8001)
    SYMBOLIC_INTERNAL_PORT: Port for the internal FastAPI server (default: 9000)
    OPENAI_API_KEY: Required for LLM operations.

Security and Logging:
    - Incoming requests are logged with method and path.
    - Ensure OPENAI_API_KEY is secured.
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
FLASK_PORT = int(os.getenv("FLASK_PORT", 8001))
SYMBOLIC_INTERNAL_PORT = int(os.getenv("SYMBOLIC_INTERNAL_PORT", 9000))
FASTAPI_HOST = "127.0.0.1"
SYMBOLIC_URL = f"http://{FASTAPI_HOST}:{SYMBOLIC_INTERNAL_PORT}"


app = Flask(__name__)
# Security: enforce HTTPS & default security headers
Talisman(app, force_https=True)

def run_symbolic_service():
    """Start the Symbolic AI FastAPI service with Uvicorn."""
    cmd = [
        "uvicorn",
        "backend.symbolic_service:app",
        "--host", FASTAPI_HOST,
        "--port", str(SYMBOLIC_INTERNAL_PORT)
    ]
    subprocess.Popen(cmd, cwd=os.getcwd())


@app.before_request
def log_request():
    logger.info(f"Received {request.method} request on {request.path}")

@app.route('/', defaults={'path': ''}, methods=['GET','POST','PUT','PATCH','DELETE'])
@app.route('/<path:path>', methods=['GET','POST','PUT','PATCH','DELETE'])
def proxy(path):
    """Proxy all requests to the internal Symbolic AI FastAPI service."""
    target = f"{SYMBOLIC_URL}/{path}"
    resp = requests.request(
        method=request.method,
        url=target,
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        params=request.args,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )
    excluded = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(n, v) for n, v in resp.headers.items() if n.lower() not in excluded]
    return Response(resp.content, resp.status_code, headers)

@app.route('/healthz', methods=['GET'])
def healthz():
    """Health check endpoint."""
    return {'status': 'ok'}

if __name__ == "__main__":
    # Launch the internal Symbolic AI FastAPI server in background, then start Flask proxy
    thread = threading.Thread(target=run_symbolic_service, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=FLASK_PORT)