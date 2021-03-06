"""
Django settings for project_noe project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from .config import config

# https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
DEBUG = config.debug
SECRET_KEY = config.secret_key

if config.sentry_dsn_url:
    sentry_sdk.init(
        dsn=config.sentry_dsn_url,
        integrations=[DjangoIntegration()],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        # We are not interested in Users, we are interested in errors during registrations,
        # which don't have Users associated with them.
        send_default_pii=False,
    )


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "django_filters",
    "appointments",
    "surveys",
    "samples",
    "payments",
    "billing",
    "users",
]

if config.debug:
    INSTALLED_APPS += ["rosetta"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

FRONTEND_URL = config.frontend_url
BACKEND_URL = config.backend_url

ALLOWED_HOSTS = config.allowed_hosts

if config.allowed_cors_hosts:
    INSTALLED_APPS += ["corsheaders"]
    MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE
    CORS_ORIGIN_WHITELIST = config.allowed_cors_hosts

if config.behind_tls_proxy:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ROOT_URLCONF = "project_noe.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project_noe.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config.database.engine,
        "NAME": config.database.name,
        "USER": config.database.user,
        "PASSWORD": config.database.password,
        "HOST": config.database.host,
        "PORT": config.database.port,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = config.language_code
TIME_ZONE = config.time_zone

USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    "locale/",
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = config.static.url
STATIC_ROOT = config.static.root

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "/admin/"
LOGOUT_URL = "/admin/logout/"

LOGGING = {
    # fmt: off
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": config.log_level,
    },
}


REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

DEFAULT_TIME_SLOT_CAPACITY = config.default_time_slot_capacity


EMAIL_BACKEND = config.email.backend
EMAIL_HOST = config.email.host
EMAIL_PORT = config.email.port
EMAIL_HOST_USER = config.email.user
EMAIL_HOST_PASSWORD = config.email.password
EMAIL_USE_TLS = config.email.use_tls
DEFAULT_FROM_EMAIL = config.email.default_from

EMAIL_VERIFICATION_KEY = config.email.verification_key

SZAMLAZZHU_AGENT_KEY = config.szamlazzhu.agent_key
SZAMLAZZHU_INVOICE_PREFIX = config.szamlazzhu.invoice_prefix

SIMPLEPAY_MERCHANT = config.simplepay.merchant
SIMPLEPAY_SECRET_KEY = config.simplepay.secret_key
SIMPLEPAY_IPN_URL = config.simplepay.ipn_url
SIMPLEPAY_USE_LIVE = config.simplepay.use_live
