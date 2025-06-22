FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Using Python slim variant for minimal footprint and security
# Install dependencies
WORKDIR /app
COPY services/frontend_service/requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
 && pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
# Copy frontend application
COPY services/frontend_service/frontend /app/frontend
# Copy core backend code for direct imports (backend.*)
COPY services/backend_core_service/backend /app/backend

# Expose Streamlit port
EXPOSE 8501

# Healthcheck for container (ensure the Streamlit app is running)
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8501/ || exit 1

# Launch Streamlit UI directly on 0.0.0.0:8501 (WebSocket support)
CMD ["streamlit", "run", "/app/frontend/app.py", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0", \
     "--server.enableCORS", "false", \
     "--server.enableXsrfProtection", "false"]