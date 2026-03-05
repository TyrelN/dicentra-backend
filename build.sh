#!/usr/bin/env bash
# Render build script for Django backend
# https://render.com/docs/deploy-django

set -o errexit

# Install dependencies (generate requirements.txt from Poetry if needed)
if [ -f pyproject.toml ]; then
  pip install poetry
  poetry export -f requirements.txt -o requirements.txt --without-hashes
fi
pip install -r requirements.txt

# Collect static files (uploads to Cloudinary if configured, or to staticfiles for WhiteNoise)
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate
