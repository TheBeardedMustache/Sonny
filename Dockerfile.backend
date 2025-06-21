FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Copy application code
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Launch backend API service
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]