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
import subprocess
import os
from flask import Flask, redirect, request

# Configuration
FLASK_PORT = int(os.getenv("FLASK_PORT", 8501))
STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8502))
STREAMLIT_HOST = "127.0.0.1"
STREAMLIT_URL = f"http://{STREAMLIT_HOST}:{STREAMLIT_PORT}"

app = Flask(__name__)

def run_streamlit():
    """Start the Streamlit app in a separate process."""
    cmd = [
        "streamlit", "run", "frontend/app.py",
        "--server.port", str(STREAMLIT_PORT),
        "--server.address", STREAMLIT_HOST,
        "--server.enableCORS", "false"
    ]
    subprocess.Popen(cmd, cwd=os.getcwd())


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    """Redirect all incoming requests to the Streamlit server."""
    return redirect(f"{STREAMLIT_URL}/{path}")

if __name__ == "__main__":
    # Launch the Streamlit server in background, then start Flask proxy
    thread = threading.Thread(target=run_streamlit, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=FLASK_PORT)