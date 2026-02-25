# Docker Setup Guide

This guide explains how to run PromptLab using Docker and Docker Compose.

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

Install Docker Desktop from: https://www.docker.com/products/docker-desktop

## Quick Start

### Development Mode (with hot reload)

```bash
# Start the application
docker-compose up

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop the application
docker-compose down
```

The API will be available at: http://localhost:8000
Interactive docs at: http://localhost:8000/docs

### Production Mode

```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

## Docker Files Explained

### `backend/Dockerfile`
Production-ready image:
- Based on Python 3.11 slim
- Optimized for size and security
- No hot reload
- Includes health checks

### `backend/Dockerfile.dev`
Development image:
- Includes hot reload support
- Faster rebuild times
- Volume mounts for live code updates

### `docker-compose.yml`
Development configuration:
- Hot reload enabled
- Source code mounted as volumes
- Port 8000 exposed

### `docker-compose.prod.yml`
Production configuration:
- No volume mounts
- Resource limits
- Always restart policy

## Common Commands

### Build and Run

```bash
# Build images
docker-compose build

# Rebuild without cache
docker-compose build --no-cache

# Start services
docker-compose up

# Start in detached mode
docker-compose up -d
```

### Managing Containers

```bash
# List running containers
docker-compose ps

# Stop services
docker-compose stop

# Start stopped services
docker-compose start

# Restart services
docker-compose restart

# Remove containers
docker-compose down

# Remove containers and volumes
docker-compose down -v
```

### Logs and Debugging

```bash
# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# View logs for specific service
docker-compose logs backend

# Execute commands in container
docker-compose exec backend bash

# Run Python shell
docker-compose exec backend python

# Run tests in container
docker-compose exec backend pytest tests/ -v
```

### Database and Data

```bash
# Run database migrations (when added)
docker-compose exec backend python -m alembic upgrade head

# Seed data
docker-compose exec backend python seed_data.py
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Application
ENV=development
DEBUG=true

# API
API_HOST=0.0.0.0
API_PORT=8000

# Database (when added)
# DATABASE_URL=postgresql://user:password@db:5432/promptlab
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Map to different host port
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Rebuild image
docker-compose build --no-cache backend

# Remove all containers and rebuild
docker-compose down
docker-compose up --build
```

### Hot Reload Not Working

Ensure volumes are properly mounted in docker-compose.yml:
```yaml
volumes:
  - ./backend/app:/app/app
```

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

## Performance Tips

### Speed Up Builds

1. Use `.dockerignore` to exclude unnecessary files
2. Order Dockerfile commands from least to most frequently changing
3. Use multi-stage builds for production

### Reduce Image Size

```bash
# View image size
docker images | grep promptlab

# Remove unused images
docker image prune

# Remove all unused data
docker system prune -a
```

## CI/CD Integration

### GitHub Actions

The CI workflow can build and test Docker images:

```yaml
- name: Build Docker image
  run: docker build -t promptlab-backend ./backend

- name: Run tests in Docker
  run: docker run promptlab-backend pytest tests/ -v
```

### Deployment

For production deployment:

```bash
# Build production image
docker build -f backend/Dockerfile -t promptlab-backend:latest ./backend

# Tag for registry
docker tag promptlab-backend:latest registry.example.com/promptlab-backend:latest

# Push to registry
docker push registry.example.com/promptlab-backend:latest
```


**Docker concepts:**
- `Dockerfile` = Instructions to build image (like a recipe)
- `docker-compose.yml` = Multi-container orchestration (like running multiple services)
- Image = Built package (like a compiled app)
- Container = Running instance (like a running process)


**Benefits:**
- Consistent environment across dev/staging/prod
- Easy onboarding (no "works on my machine")
- Isolated dependencies
- Easy scaling and deployment
