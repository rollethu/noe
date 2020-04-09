resource "aws_lb_listener" "backend" {
  for_each          = var.app_tg_ports
  load_balancer_arn = local.core_config.ecs_cluster_private_nlb.arn
  port              = each.key
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_nlb_tgs[each.key].arn
  }
}

resource "aws_lb_target_group" "backend_nlb_tgs" {
  for_each    = var.app_tg_ports
  name        = "${var.app_name}-${terraform.workspace}-tg-${each.key}"
  target_type = "instance"
  port        = each.key
  protocol    = "TCP"
  vpc_id      = local.core_config.vpc.vpc_id
  health_check {
    enabled             = true
    interval            = 10
    protocol            = "HTTP"
    healthy_threshold   = 3
    unhealthy_threshold = 3
    path                = "/health/"
  }
  deregistration_delay = var.cooldown_seconds
}
