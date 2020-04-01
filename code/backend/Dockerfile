FROM python:3.7-alpine

WORKDIR /project-noe/backend
COPY requirements/requirements.development.txt requirements.txt

RUN pip install -r requirements.txt

CMD ./manage.py runserver 0.0.0.0:8000