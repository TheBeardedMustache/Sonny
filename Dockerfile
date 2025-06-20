FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir -e /app

# Copy code explicitly
COPY . /app

# Expose necessary ports
EXPOSE 8501 8000

# Backend startup explicitly
CMD ["sh", "-c", "\
    uvicorn backend.api:app --host 0.0.0.0 --port 8000 & \
    cd frontend && streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.enableCORS=false"]

# Healthcheck explicitly verifies backend availability
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8000/ || exit 1
