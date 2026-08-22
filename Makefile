SHELL := /bin/bash

.PHONY: setup up down logs test lint format typecheck seed migrate eval build clean

setup:
	cp -n .env.example .env || true

up: setup
	docker compose -f docker/docker-compose.yml up --build -d

down:
	docker compose -f docker/docker-compose.yml down

logs:
	docker compose -f docker/docker-compose.yml logs -f

build:
	docker compose -f docker/docker-compose.yml build

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .

typecheck:
	mypy src config

seed:
	python scripts/seed_database.py

migrate:
	alembic -c alembic.ini upgrade head

eval:
	python scripts/evaluate_rag.py

clean:
	docker compose -f docker/docker-compose.yml down -v --remove-orphans
