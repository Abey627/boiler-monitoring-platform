# Docker Setup

## Quick Start

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up --build -d

# Stop all services
docker-compose down
```

## Access URLs

- **Dashboard:** http://localhost/
- **Health Checks:**
  - Frontend API: http://localhost/api/frontend/health/
  - IoT Ingestion: http://localhost/api/iot/health/
  - AI Processor: http://localhost/api/ai/health/
  - Alert Service: http://localhost/api/alert/health/

## Useful Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f frontend_web

# Restart service
docker-compose restart frontend_web

# Rebuild service
docker-compose up --build frontend_web

# Execute commands in container
docker-compose exec frontend_web python manage.py shell

# Check container status
docker-compose ps

# Clean up
docker-compose down -v
```
