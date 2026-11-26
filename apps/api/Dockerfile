# Build context: repository root (see infrastructure/docker-compose.yml).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY apps/api/pyproject.toml ./
# Install third-party dependencies first for layer caching.
RUN python - <<'EOF' > /tmp/requirements.txt
import tomllib
print("\n".join(tomllib.load(open("pyproject.toml", "rb"))["project"]["dependencies"]))
EOF
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY apps/api/ ./

RUN useradd --create-home --uid 10001 app \
    && mkdir -p /data/storage /data/outbox \
    && chown -R app:app /data /app
USER app

EXPOSE 8000

# Migrate, then serve. ENVIRONMENT=local is set by Compose.
CMD ["sh", "-c", "alembic upgrade head && uvicorn api.main:app --host 0.0.0.0 --port 8000"]
