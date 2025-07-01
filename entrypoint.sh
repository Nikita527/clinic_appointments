#!/bin/sh
set -e

# Ожидание готовности БД
echo "Waiting for database to be ready..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

alembic upgrade head
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
