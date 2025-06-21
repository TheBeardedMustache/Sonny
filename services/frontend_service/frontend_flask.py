"""
frontend_flask.py: Flask wrapper for serving the Streamlit-based frontend.
This wrapper starts the Streamlit app in a background thread and proxies
all HTTP requests to the Streamlit server for a seamless unified entry point.

Endpoints:
    Any path: Proxy to the Streamlit server.

Environment Variables:
    FLASK_PORT: Port for the Flask server (default: 8501)
    STREAMLIT_PORT: Port for the Streamlit server (default: 8502)

Security:
    - In production, consider adding authentication and HTTPS.
"""

import threading
import logging
import subprocess
import os
from flask import Flask, request, Response
from flask_talisman import Talisman
import requests
from pythonjsonlogger import jsonlogger

# Configuration
FLASK_PORT = int(os.getenv("FLASK_PORT", 8501))
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8502))
STREAMLIT_HOST = "127.0.0.1"
STREAMLIT_URL = f"http://{STREAMLIT_HOST}:{STREAMLIT_PORT}"

app = Flask(__name__)
# Security: enforce HTTPS & default security headers
env = os.getenv("FLASK_ENV", "development")
force_https = env.lower() == "production"
Talisman(app, force_https=force_https, strict_transport_security=force_https)

# Structured JSON logging
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = [handler]

def run_streamlit():
    """Start the Streamlit app in a separate process."""
    cmd = [
        "streamlit", "run", "frontend/app.py",
        "--server.port", str(STREAMLIT_PORT),
        "--server.address", STREAMLIT_HOST,
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    subprocess.Popen(cmd, cwd=os.getcwd())


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    """Reverse-proxy all incoming requests to the internal Streamlit server."""
    target_url = f"{STREAMLIT_URL}/{path}"
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
    headers = [(name, value) for name, value in resp.headers.items() if name.lower() not in excluded]
    return Response(resp.content, resp.status_code, headers)

@app.route('/healthz', methods=['GET'])
def healthz():
    """Health check endpoint."""
    return {'status': 'ok'}

if __name__ == "__main__":
    # Launch the Streamlit server in background, then start Flask proxy
    thread = threading.Thread(target=run_streamlit, daemon=True)
    thread.start()
    logger.info(f"Flask proxy listening on http://0.0.0.0:{FLASK_PORT}")
    app.run(host="0.0.0.0", port=FLASK_PORT)