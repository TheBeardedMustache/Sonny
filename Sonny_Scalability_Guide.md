# Sonny Scalability Guide

## Environment Variable Port Overrides

- `FRONTEND_PORT`: external port for the Streamlit frontend proxy (default: 8501)
- `BACKEND_PORT`: external port for the Backend Core proxy (default: 8000)
- `SYMBOLIC_PORT`: external port for the Symbolic AI proxy (default: 8001)

Configure these in your `.env` file to resolve port conflicts or customize mappings.

This guide outlines horizontal scaling and load‑balancing strategies for Sonny's microservices architecture.

## 1. Docker‑Compose Replication

### Service Replicas

By using the `deploy.replicas` directive in `docker-compose.yml` (version 3.8+), you can specify the number of container instances per service:

```yaml
services:
  frontend_service:
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
      update_config:
        parallelism: 2
        delay: 10s
```

### Dynamic Scaling

To adjust replicas at runtime (Compose v1.28+):

```bash
# Scale frontend to 5 instances
docker-compose up --scale frontend_service=5 -d

# Scale backend_core_service to 4 instances
docker-compose up --scale backend_core_service=4 -d
```

## 2. Docker Swarm (Production Orchestration)

Using Docker Swarm yields native load‑balancing and advanced scheduling:

```bash
docker swarm init
docker stack deploy -c docker-compose.yml sonny
```

Swarm automatically distributes requests across replicas and reconciles state.

## 3. External Load Balancer

For vanilla Compose (non‑Swarm), front your services with a reverse proxy (e.g., Traefik, NGINX) to distribute traffic:

```yaml
services:
  traefik:
    image: traefik:v2.9
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
```

## 4. Autoscaling Considerations

Autonomous scaling typically requires external metrics‑based tooling (e.g., Kubernetes HPA, Docker Autoscaler).

## 5. Best Practices

- Monitor container health (via `docker-compose ps`, healthchecks).
- Ensure idempotent startup logic for multiple replicas.
- Implement graceful shutdown handling.
- Centralize logging and metrics to identify load hotspots.