app_name      = "noe-grafana"
app_image_url = "docker.io/grafana/grafana:latest"
env_vars = {
  GF_INSTALL_PLUGINS = "grafana-clock-panel,grafana-simple-json-datasource"

}

env_secrets = {}

app_tg_ports = {
  "3000" = {
    protocol  = "tcp"
    host_port = 0
  }
}

desired_count    = 1
minimum_percent  = 0
maximum_percent  = 150
cooldown_seconds = 1

cw_log_group_name   = "noe-ecs-private-cluster"
cw_log_group_region = "eu-central-1"
