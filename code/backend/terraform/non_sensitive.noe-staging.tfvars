app_name      = "noe-backend"
env_vars = {
  DJANGO_DATABASE_HOST    = "noe-staging-postgres.co7irzuctvdj.eu-central-1.rds.amazonaws.com"
  DJANGO_DATABASE_PORT    = "5432"
  DJANGO_DATABASE_USER    = "noe_master"
  DJANGO_DATABASE_NAME    = "noe_db"
  ALLOWED_CORS_HOSTS      = "https://noe.rollet.app"
  EMAIL_BACKEND           = "django_ses.SESBackend"
  FRONTEND_URL            = "https://noe.rollet.app"
  AWS_SES_REGION_NAME     = "eu-central-1"
  AWS_SES_REGION_ENDPOINT = "email.eu-central-1.amazonaws.com"
}

env_secrets = {
  DJANGO_SECRET_KEY         = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/django_secret_key"
  DJANGO_DATABASE_PASSWORD  = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/django_database_password"
  EMAIL_VERIFICATION_KEY    = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-staging/backend/email_verification_key"
  AWS_SES_ACCESS_KEY_ID     = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-common/backend/aws-ses-iam-access-key-id"
  AWS_SES_SECRET_ACCESS_KEY = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe-common/backend/aws-ses-iam-secret-access-key"
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
