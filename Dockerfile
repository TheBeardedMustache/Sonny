# Dockerfile: Encapsulation of Sonny platform in container
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Expose ports for Streamlit and API
EXPOSE 8501 8000

# Default command to run the Streamlit application
CMD ["sh", "-c", \
    "uvicorn backend.api:app --host 0.0.0.0 --port 8000 & \
     streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0"]

# Healthcheck to ensure API is responsive
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8000/ || exit 1