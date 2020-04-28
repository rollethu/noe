variable "app_name" {
}
variable "app_tg_ports" {
  default = {
    80 = {
      protocol  = "tcp"
      host_port = 80
    }
    443 = {
      protocol  = "tcp"
      host_port = 443
    }
  }
}
variable "app_image_url" {}

variable "env_vars" {
  default = {
    APP_FQDN             = "asdf"
    BACKEND_APP_ALB_FQDN = "asdf.asdf.asdf"
    BACKEND_APP_ALB_PORT = "8000"
  }
}

variable "env_secrets" {
  type        = map
  default     = {}
  description = "environment_variable_name = ssm_arn"
}

variable "cooldown_seconds" {
  default     = 60
  description = "Seconds to wait before the target group releases a container when scaling-in/deploying"
}

variable "cw_log_group_name" {
  description = "CloudWatch Log Group to send logs to"
}
variable "cw_log_group_region" {
  description = " The region of the CloudWatch Log Group to send logs to"
}
variable "desired_count" {
  description = "Number of tasks to start"
}
variable "minimum_percent" {
  description = "This percentage of the desired tasks will keep running unless stopped manually"
}
variable "maximum_percent" {
  description = "We can scale up to a maximum this percentage of the task"
}