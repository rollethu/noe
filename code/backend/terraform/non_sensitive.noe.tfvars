app_name      = "juice-backend"
app_image_url = "074164835766.dkr.ecr.eu-west-3.amazonaws.com/juice-backend2:latest"
env_vars = {
  DJANGO_DATABASE_HOST = "dev-db.cwcdru6hbnif.eu-west-1.rds.amazonaws.com"
  DJANGO_DATABASE_PORT = "3306"
  DJANGO_DATABASE_USER = "admin"
}

env_secrets = {
  DJANGO_SECRET_KEY        = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/django_secret_key"
  DJANGO_DATABASE_PASSWORD = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/django_database_password"
}

app_tg_ports = {
  "8000" = {
    protocol  = "tcp"
    host_port = 0
  }
}

desired_count    = 3
cooldown_seconds = 3

cw_log_group_name   = "noe-ecs-private-cluster"
cw_log_group_region = "eu-central-1"
