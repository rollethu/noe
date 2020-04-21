FROM python:3.8-slim
ARG COMMIT=""
ARG BRANCH=""
ARG BUILD=""
ARG STATIC_URL=""

ENV POETRY_VIRTUALENVS_CREATE=false

ENV COMMIT=${COMMIT}
ENV BRANCH=${BRANCH}
ENV BUILD=${BUILD}
ENV STATIC_URL=${STATIC_URL}

WORKDIR /project-noe/backend
COPY . .

RUN pip install poetry
RUN poetry install --no-dev


CMD ./entrypoint.sh
