.PHONY: help build up down logs test clean restart shell

# Default target
help:
	@echo "PromptLab Docker Commands"
	@echo "========================="
	@echo "make build       - Build Docker images"
	@echo "make up          - Start development environment"
	@echo "make down        - Stop all containers"
	@echo "make logs        - View container logs"
	@echo "make test        - Run tests in container"
	@echo "make shell       - Open shell in backend container"
	@echo "make restart     - Restart all containers"
	@echo "make clean       - Remove containers and volumes"
	@echo "make prod-up     - Start production environment"
	@echo "make prod-down   - Stop production environment"

# Development commands
build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✓ Backend running at http://localhost:8000"
	@echo "✓ API docs at http://localhost:8000/docs"

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose exec backend pytest tests/ -v --cov=app --cov-report=term-missing

shell:
	docker-compose exec backend bash

restart:
	docker-compose restart

clean:
	docker-compose down -v
	docker system prune -f

# Production commands
prod-up:
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✓ Production backend running at http://localhost:8000"

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f
