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

# This is a workaround for missing wheels for cryptography 2.9.1
RUN pip install cryptography==2.9
RUN pip install poetry
RUN poetry install --no-dev


CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "project_noe.wsgi"]
