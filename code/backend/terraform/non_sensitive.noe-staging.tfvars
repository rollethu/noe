app_name      = "noe-backend"
env_vars = {
  DJANGO_DATABASE_HOST = "noe-staging-postgres.co7irzuctvdj.eu-central-1.rds.amazonaws.com"
  DJANGO_DATABASE_PORT = "5432"
  DJANGO_DATABASE_USER = "noe_master"
  ALLOWED_CORS_HOSTS   = "https://noe.rollet.app"
  EMAIL_BACKEND        = "django.core.mail.backends.console.EmailBackend"
  FRONTEND_URL         = "https://noe.rollet.app"
}

env_secrets = {
  DJANGO_SECRET_KEY        = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/django_secret_key"
  DJANGO_DATABASE_PASSWORD = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/django_database_password"
  EMAIL_VERIFICATION_KEY   = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/email_verification_key"
}

app_tg_ports = {
  "8000" = {
    protocol  = "tcp"
    host_port = 0
  }
}

desired_count    = 1
cooldown_seconds = 3

cw_log_group_name   = "noe-staging-ecs-private-cluster"
cw_log_group_region = "eu-central-1"
