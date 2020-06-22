FROM python:3.8-slim
ARG COMMIT=""
ARG BRANCH=""
ARG BUILD=""

ENV POETRY_VIRTUALENVS_CREATE=false

ENV COMMIT=${COMMIT}
ENV BRANCH=${BRANCH}
ENV BUILD=${BUILD}

WORKDIR /project_noe/backend
RUN mkdir /project_noe/static_root

COPY pyproject.toml poetry.lock /project_noe/backend/

COPY online-payments /project_noe/backend/online-payments

RUN pip install poetry
RUN poetry install --no-dev

COPY . /project_noe/backend

RUN ["./collectstatic.sh"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "project_noe.wsgi"]
