#!/usr/bin/env sh
set -eu
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi
docker compose -f docker/docker-compose.yml up --build -d
echo "UI:     http://localhost:8501"
echo "API:    http://localhost:8000/docs"
echo "MLflow: http://localhost:5000"
echo "Qdrant: http://localhost:6333/dashboard"
echo "Seed demo user: docker compose -f docker/docker-compose.yml exec api python scripts/seed_database.py"
