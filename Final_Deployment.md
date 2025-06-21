## Final Deployment Instructions

Sonny is modularized into three microservices:
1. Frontend Service (`sonny-frontend`)
2. Backend Core Service (`sonny-backend`)
3. Symbolic AI Service (`sonny-symbolic`)

### Prerequisites
- Docker and Docker Compose installed.
- `.env` file with `OPENAI_API_KEY`.

### Build Microservices
- Frontend: `docker build -f Dockerfile.frontend -t sonny-frontend .`
- Backend Core: `docker build -f Dockerfile.backend -t sonny-backend .`
- Symbolic AI: `docker build -f Dockerfile.symbolic -t sonny-symbolic .`

### Run Microservices
- `docker run -d --name sonny-frontend --env-file .env -p 8501:8501 sonny-frontend`
- `docker run -d --name sonny-backend --env-file .env -p 8000:8000 sonny-backend`
- `docker run -d --name sonny-symbolic --env-file .env -p 9000:9000 sonny-symbolic`

### Orchestration with Docker Compose
Create a `docker-compose.yml` file with contents:
  version: '3.8'
  services:
    frontend:
      image: sonny-frontend
      ports:
        - '8501:8501'
      env_file: .env
    backend:
      image: sonny-backend
      ports:
        - '8000:8000'
      env_file: .env
    symbolic:
      image: sonny-symbolic
      ports:
        - '9000:9000'
      env_file: .env
- Run: `docker-compose up -d`

### Verification
- UI: http://localhost:8501
- API: http://localhost:8000/process/
- Symbolic AI: http://localhost:9000/interpret/

### Cleanup
- `docker-compose down --volumes`