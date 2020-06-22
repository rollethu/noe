#!/usr/bin/env bash

export DJANGO_DEBUG=false
export SECRET_KEY="doesnmatterforcollectstatic"
export LOG_LEVEL="DEBUG"

export EMAIL_BACKEND="console"
export EMAIL_HOST="doesnmatterforcollectstatic"
export EMAIL_DEFAULT_FROM="doesnmatterforcollectstatic"
export EMAIL_VERIFICATION_KEY="78wdidbLyLE-Pe1LSgSru5Cqspya5hFGKtydrP-48Rc="

export FRONTEND_URL="doesnmatterforcollectstatic"
export BACKEND_URL="doesnmatterforcollectstatic"

export DATABASE_ENGINE="sqlite"
export DATABASE_NAME="db.sqlite3"

export STATIC_ROOT=/project_noe/static_root
export ALLOWED_CORS_HOSTS="doesnmatterforcollectstatic"

export SZAMLAZZHU_AGENT_KEY="doesnmatterforcollectstatic"
export SZAMLAZZHU_INVOICE_PREFIX="doesnmatterforcollectstatic"

export SIMPLEPAY_ENVIRONMENT="sandbox"
export SIMPLEPAY_MERCHANT="doesnmatterforcollectstatic"
export SIMPLEPAY_SECRET_KEY="doesnmatterforcollectstatic"
export SIMPLEPAY_IPN_URL="doesnmatterforcollectstatic"

./manage.py collectstatic --link
