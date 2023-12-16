#!/bin/bash
# Upgrade to latest migration version
poetry run alembic -c /app/secrets/alembic.ini upgrade head