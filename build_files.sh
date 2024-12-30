#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install system dependencies
apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
python3.9 -m venv /opt/venv
source /opt/venv/bin/activate

# Install Poetry and generate requirements.txt
pip install --upgrade pip
pip install poetry
poetry export -f requirements.txt --output requirements.txt

# Install Python dependencies
pip install -r requirements.txt

# Remove Poetry to save space
pip uninstall -y poetry

# Optional: Collect static files if needed for Django
python manage.py collectstatic --no-input