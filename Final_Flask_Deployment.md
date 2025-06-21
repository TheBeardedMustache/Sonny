# Final Flask Deployment

This document describes how to deploy and manage the Flask-encapsulated microservices for the Sonny project.

## Prerequisites

- Docker and Docker Compose installed.
- An .env file at the project root with the OPENAI_API_KEY variable set.

## Building and Starting Services

Use the provided setup script to build and launch all Flask-wrapped services:

```bash
./setup_flask_services.sh
```

This command will:
- Build Docker images for frontend_service, backend_core_service, and symbolic_ai_service.
- Launch containers for each service with ports exposed.

## Service Endpoints

| Service               | Port  | Description                                  |
|-----------------------|-------|----------------------------------------------|
| Frontend Service      | 8501  | Streamlit UI via Flask wrapper               |
| Backend Core Service  | 8000  | FastAPI core via Flask proxy                 |
| Symbolic AI Service   | 8001  | Symbolic AI FastAPI via Flask proxy          |

## Managing Services

Use Docker Compose commands for operations:

```bash
# View running services
docker-compose ps

# Stop and remove services
docker-compose down

# Rebuild and restart services
docker-compose up --build

# View logs in real-time
docker-compose logs -f
```