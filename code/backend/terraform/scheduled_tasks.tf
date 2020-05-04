resource "aws_cloudwatch_event_rule" "cw_rules"{
    for_each = var.scheduled_tasks_to_run
    name_prefix = "${var.app_name}-${terraform.workspace}-cwr-"
    schedule_expression = each.value.cron
}

resource "aws_iam_role" "ecs_events" {
  count = var.scheduled_tasks_to_run == {} ? 0 : 1  

  name = "ecs_events"
  assume_role_policy = <<DOC
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "events.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
DOC
}

resource "aws_iam_role_policy" "ecs_events_run_task_with_any_role" {
  count = var.scheduled_tasks_to_run == {} ? 0 : 1  
  name = "ecs_events_run_noe_tasks"
  role = aws_iam_role.ecs_events[0].id

  policy = <<DOC
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "${aws_iam_role.task_execution_role.arn}"
        },
        {
            "Effect": "Allow",
            "Action": "ecs:RunTask",
            "Resource": "${replace(module.backend_app.td_arn, "/:\\d+$/", ":*")}"
        }
    ]
}
DOC
}

resource "aws_cloudwatch_event_target" "ecs_scheduled_task" {
  for_each  = var.scheduled_tasks_to_run
  target_id = "${var.app_name}-${terraform.workspace}-st-${each.value.task_name}"
  arn       = data.aws_ecs_cluster.private_cluster.arn
  rule      = aws_cloudwatch_event_rule.cw_rules[each.key].name
  role_arn  = aws_iam_role.ecs_events[0].arn

  ecs_target {
    task_count          = 1
    task_definition_arn = module.backend_app.td_arn
    group = "scheduled_tasks"
  }

  input = <<DOC
{
  "containerOverrides": [
    {
      "name": "${module.backend_app.app_container_name}",
      "command": ${jsonencode(each.value.command)}
    }
  ]
}
DOC
}