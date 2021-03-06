app_name = "noe-backend"
env_vars = {
  DJANGO_DEBUG              = "true"
  DJANGO_DATABASE_HOST      = "noe-staging-postgres.co7irzuctvdj.eu-central-1.rds.amazonaws.com"
  DJANGO_DATABASE_PORT      = "5432"
  DJANGO_DATABASE_USER      = "noe_master"
  DJANGO_DATABASE_NAME      = "noe_db"
  ALLOWED_CORS_HOSTS        = "https://noe.rollet.app"
  EMAIL_BACKEND             = "django.core.mail.backends.smtp.EmailBackend"
  FRONTEND_URL              = "https://noe.rollet.app"
  BACKEND_URL               = "https://api.noe.rollet.app"
  DJANGO_EMAIL_HOST         = "email-smtp.eu-central-1.amazonaws.com"
  DJANGO_EMAIL_PORT         = "587"
  DJANGO_EMAIL_USE_TLS      = "true"
  DJANGO_DEFAULT_FROM_EMAIL = "no-reply@tesztallomas.hu"
  SENTRY_DSN_URL            = ""
  SZAMLAZZHU_INVOICE_PREFIX = "TSZTP"
  SIMPLEPAY_ENVIRONMENT     = "sandbox"
}

env_secrets = {
  DJANGO_SECRET_KEY           = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/django_secret_key"
  DJANGO_DATABASE_PASSWORD    = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/django_database_password"
  EMAIL_VERIFICATION_KEY      = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/email_verification_key"
  SZAMLAZZHU_AGENT_KEY        = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/szamlazzhu_agent_key"
  DJANGO_EMAIL_HOST_USER      = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-common/backend/aws-ses-smtp-user"
  DJANGO_EMAIL_HOST_PASSWORD  = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-common/backend/aws-ses-smtp-password"
  SIMPLEPAY_MERCHANT          = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/simplepay-merchant"
  SIMPLEPAY_SECRET_KEY        = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/simplepay-secret-key"
}

app_tg_ports = {
  "8000" = {
    protocol  = "tcp"
    host_port = 0
  }
}

desired_count    = 2
minimum_percent  = 50
maximum_percent  = 150
cooldown_seconds = 3

cw_log_group_name   = "noe-staging-ecs-private-cluster"
cw_log_group_region = "eu-central-1"
# scheduled_tasks_to_run = {
#   0 = {
#     cron      = "cron(* * * * ? *)" # every minute
#     command   = ["echo", "hello"]
#     task_name = "test"
#   }
#   1 = {
#     cron      = "cron(20 * * * ? *)"
#     task_name = "test2"
#     command   = ["echo", "hello2"]
#   }
# }
