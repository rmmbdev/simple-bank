FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VIRTUALENVS_CREATE false

COPY backend/ /app/backend/

COPY pyproject.toml /app/

ENV PYTHONPATH /app/
WORKDIR /app/

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry install --no-dev --no-interaction --no-ansi