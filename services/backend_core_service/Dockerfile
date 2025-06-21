FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flask requests

# Copy application code
COPY . /app

# Expose Flask proxy port
EXPOSE 8000

# Launch Flask proxy for FastAPI core
CMD ["python", "backend_core_flask.py"]