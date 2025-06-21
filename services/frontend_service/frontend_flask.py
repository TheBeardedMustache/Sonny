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
import requests

# Configuration
FLASK_PORT = int(os.getenv("FLASK_PORT", 8501))
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8502))
STREAMLIT_HOST = "127.0.0.1"
STREAMLIT_URL = f"http://{STREAMLIT_HOST}:{STREAMLIT_PORT}"

app = Flask(__name__)

# Logger setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

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