#! /usr/bin/env bash
set -e

# Let the DB connection start
python /service/app/backend_pre_start.py

sleep 10;

# Run migrations
alembic upgrade head
# alembic downgrade base

python /service/app/main.py