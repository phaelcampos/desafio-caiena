# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml /app/

COPY owm-0.1.0-py3-none-any.whl /app/

RUN poetry lock --no-update
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

RUN poetry add /app/owm-0.1.0-py3-none-any.whl

COPY .. /app

EXPOSE 8000

CMD poetry run uvicorn --host 0.0.0.0 api.app:app
