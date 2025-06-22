FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Using Python slim variant for minimal footprint and security
# Install dependencies
WORKDIR /app
COPY requirements.txt /app/
# Install curl for healthchecks and Python dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
 && pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask requests flask-talisman python-json-logger prometheus_client

# Copy application code
COPY . /app

# Expose Flask proxy port
EXPOSE 8000

# Healthcheck for container
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/healthz || exit 1

# Launch Flask proxy for FastAPI core
CMD ["python", "backend_core_flask.py"]