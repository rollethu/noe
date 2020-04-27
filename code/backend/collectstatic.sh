#!/usr/bin/env bash

export DJANGO_SECRET_KEY=doesnmatterforcollectstatic
export ALLOWED_CORS_HOSTS=doesnmatterforcollectstatic
export EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
export DJANGO_EMAIL_HOST=doesnmatterforcollectstatic
export DJANGO_EMAIL_PORT=doesnmatterforcollectstatic
export DJANGO_EMAIL_HOST_USER=doesnmatterforcollectstatic
export DJANGO_EMAIL_HOST_PASSWORD=doesnmatterforcollectstatic
export DJANGO_EMAIL_USE_TLS=true
export DJANGO_DEFAULT_FROM_EMAIL="doesnmatterforcollectstatic"
export LOG_LEVEL="DEBUG"
export EMAIL_VERIFICATION_KEY="78wdidbLyLE-Pe1LSgSru5Cqspya5hFGKtydrP-48Rc="
export FRONTEND_URL="doesnmatterforcollectstatic"
export BACKEND_URL="doesnmatterforcollectstatic"
export DJANGO_DEBUG=true
export DJANGO_DATABASE_ENGINE="django.db.backends.sqlite3"
export DJANGO_DATABASE_NAME="db.sqlite3"
export DJANGO_DATABASE_USER="doesnmatterforcollectstatic"
export DJANGO_DATABASE_PASSWORD="doesnmatterforcollectstatic"
export DJANGO_DATABASE_HOST="doesnmatterforcollectstatic"
export DJANGO_DATABASE_PORT=doesnmatterforcollectstatic

export STATIC_ROOT=/project_noe/static_root

./manage.py collectstatic --link
