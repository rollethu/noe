FROM python:3.8-slim

WORKDIR /project-noe/backend

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

COPY pyproject.toml poetry.lock /project-noe/backend/

RUN poetry install --no-dev

CMD ./manage.py runserver 0.0.0.0:8000
