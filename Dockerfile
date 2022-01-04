FROM python:3.9-slim-buster as base

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NOCACHE_DIR 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/* 

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY poetry.lock pyproject.toml ./
RUN pip3 install poetry && poetry export -f requirements.txt --output requirements.txt \
    && pip install -r requirements.txt && pip3 uninstall -y poetry

FROM python:3.9-slim-buster as builder
ARG ALLOWED_HOSTS
ARG CLOUD_API_KEY
ARG CLOUD_API_SECRET
ARG CLOUD_NAME
ARG CLOUDINARY_URL
ARG CORS_ALLOWED
ARG EMAIL_DOMAIN
ARG EMAIL_HOST
ARG EMAIL_HOST_PASSWORD
ARG EMAIL_HOST_USER
ARG SECRET_KEY
ARG DATABASE_URL

COPY --from=base /opt/venv /opt/venv
COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && adduser myuser
USER myuser
ENV PATH="/opt/venv/bin:$PATH"

#production command
CMD gunicorn config.wsgi:application --workers=3 --threads=2 --bind 0.0.0.0:$PORT

