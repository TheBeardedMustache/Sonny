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

# Expose Streamlit port
EXPOSE 8501

# Launch Streamlit frontend
CMD ["sh", "-c", "cd frontend && streamlit run app.py --server.port=8501 --server.address=0.0.0.0 --server.enableCORS=false"]