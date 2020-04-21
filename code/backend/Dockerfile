FROM python:3.8-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /project-noe/backend
COPY . .

RUN pip install poetry
RUN poetry install --no-dev


CMD ./entrypoint.sh
