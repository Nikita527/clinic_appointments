FROM python:3.12-slim

RUN apt-get update && apt-get install -y postgresql-client curl && rm -rf /var/lib/apt/lists/*

RUN useradd -m app

WORKDIR /app

COPY pyproject.toml poetry.lock* requirements.txt* ./
RUN pip install --upgrade pip && \
    pip install uv

RUN if [ -f pyproject.toml ]; then uv pip install --system --no-cache-dir .; \
    elif [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

COPY . .

USER app

HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=5 CMD curl -f http://localhost:8000/api/v1/health || exit 1

COPY entrypoint.sh .
ENTRYPOINT ["./entrypoint.sh"]
