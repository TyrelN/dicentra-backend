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

COPY --from=base /opt/venv /opt/venv
COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && adduser myuser
USER myuser
ENV PATH="/opt/venv/bin:$PATH"

#production command
CMD python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

