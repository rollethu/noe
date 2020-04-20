app_name      = "noe-backend"
# app_image_url = "074164835766.dkr.ecr.eu-central-1.amazonaws.com/noe-backend"
env_vars = {
  DJANGO_DATABASE_HOST = "noe-postgres.co7irzuctvdj.eu-central-1.rds.amazonaws.com"
  DJANGO_DATABASE_PORT = "5432"
  DJANGO_DATABASE_USER = "noe_master"
  ALLOWED_CORS_HOSTS   = "https://regisztracio.tesztallomas.hu"
  EMAIL_BACKEND        = "django.core.mail.backends.console.EmailBackend"
  FRONTEND_URL         = "https://regisztracio.tesztallomas.hu"
}

env_secrets = {
  DJANGO_SECRET_KEY        = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/django_secret_key"
  DJANGO_DATABASE_PASSWORD = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/django_database_password"
  EMAIL_VERIFICATION_KEY   = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/email_verification_key"
}

app_tg_ports = {
  "8000" = {
    protocol  = "tcp"
    host_port = 0
  }
}

desired_count    = 1
cooldown_seconds = 3

cw_log_group_name   = "noe-ecs-private-cluster"
cw_log_group_region = "eu-central-1"
