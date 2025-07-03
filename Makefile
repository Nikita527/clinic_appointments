help:
	@echo "Usage: make [up|down|run|test|migrate|lint]"
	@echo "up - start docker containers"
	@echo "down - stop docker containers and remove volumes"
	@echo "run - run uvicorn for local development"
	@echo "test - run pytest in docker container"
	@echo "migrate - run alembic migrations in docker container"
	@echo "lint - run ruff for linting"

up:
	docker-compose up -d --build

down:
	docker-compose down --volumes

run:
	uvicorn src.main:app --reload

test:
	docker compose exec api pytest

migrate:
	docker compose exec api alembic upgrade head

lint:
	ruff check .
	ruff format --check .

up-db:
	docker compose up -d clinic_db

.PHONY: up down run test migrate lint
