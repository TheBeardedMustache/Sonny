FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Using Python slim variant for minimal footprint and security
# Install dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask requests flask-talisman python-json-logger

# Copy application code
COPY . /app

# Expose Flask proxy port
EXPOSE 8001

# Healthcheck for container
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8001/healthz || exit 1

# Launch Flask proxy for Symbolic AI service
CMD ["python", "symbolic_ai_flask.py"]