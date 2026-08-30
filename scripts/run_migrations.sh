#!/usr/bin/env sh
set -eu
alembic -c alembic.ini upgrade head
python scripts/seed_database.py
