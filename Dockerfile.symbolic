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

# Expose Symbolic AI service port
EXPOSE 9000

# Launch symbolic AI microservice
CMD ["uvicorn", "backend.symbolic_service:app", "--host", "0.0.0.0", "--port", "9000"]