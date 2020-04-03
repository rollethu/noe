app_name      = "juice-backend"
app_image_url = "074164835766.dkr.ecr.eu-west-3.amazonaws.com/juice-backend2:latest"
env_vars = {
  DJANGO_SETTINGS_MODULE            = "juice.settings.production"
  DJANGO_DATABASE_NAME              = "juice"
  # AWS_IOS_PLATFORM_APPLICATION_ARN  = "arn:aws:sns:us-east-1:074164835766:app/APNS/juice-test-ios"
  # AWS_IOS_PUSH_NOTIFICATION_SERVICE = "APNS"
  AWS_IOS_PLATFORM_APPLICATION_ARN  = "arn:aws:sns:us-east-1:074164835766:app/APNS_SANDBOX/juice-dev-ios"
  AWS_IOS_PUSH_NOTIFICATION_SERVICE = "APNS_SANDBOX"
  DEFAULT_FILE_STORAGE              = "storages.backends.s3boto3.S3Boto3Storage"
  AWS_STORAGE_BUCKET_NAME           = "rlt-juice"
  AWS_LOCATION                      = "files"
  AWS_S3_REGION_NAME                = "eu-west-3"
  AWS_SNS_REGION_NAME               = "us-east-1"
  ROLLET_BASE_URL                   = "https://dev.rollet.app/api/v1/platform/"
  LANG                              = "C.UTF-8"
  DJANGO_DATABASE_HOST              = "dev-db.cwcdru6hbnif.eu-west-1.rds.amazonaws.com"
  DJANGO_DATABASE_PORT              = "3306"
  DJANGO_DATABASE_USER              = "admin"
  REDIS_HOST                        = "dev-redis.8iaq37.0001.euw1.cache.amazonaws.com"
  REDIS_PORT                        = "6379"
  FEEDBACK_EMAIL_ADDRESSES          = "richard.szabacsik@rollet.hu"
  REDIS_PASSWORD                    = ""
}

env_secrets = {
  DJANGO_SECRET_KEY                              = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/backend/django_secret_key"
  DJANGO_DATABASE_PASSWORD                       = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/backend/django_database_password"
  ROLLET_AUTH_TOKEN                              = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/rollet_auth_token"
  AWS_ACCESS_KEY_ID                              = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/aws_secret_id"
  AWS_SECRET_ACCESS_KEY                          = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/aws_secret_key"
  SENTRY_URL                                     = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/sentry_url"
  DAILY_COMPLETED_FUELING_REPORT_EMAIL_ADDRESSES = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/daily_completed_fueling_report_email_addresses"
  DAILY_ALL_FUELING_REPORT_EMAIL_ADDRESSES       = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/daily_all_fueling_report_email_addresses"
  GPG_KEY                                        = "arn:aws:ssm:eu-west-3:074164835766:parameter/juice/dev/gpg_key"
}

app_tg_ports = {
  "8000" = {
    protocol  = "tcp"
    host_port = 0
  }
}

desired_count    = 2
cooldown_seconds = 3

cw_log_group_name   = "dev-ecs-pri-cluster"
cw_log_group_region = "eu-west-1"