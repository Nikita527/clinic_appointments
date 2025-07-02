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
