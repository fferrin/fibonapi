# SNS Configuration
resource "aws_sns_topic" "cloudwatch_alerts_topic" {
  name = "${local.config.env}-Default_CloudWatch_Alarms_Topic"
  tags = local.tags
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "ec2_healthcheck_failure" {
  count               = local.config.env != "dev" ? 1 : 0
  alarm_name          = "${local.config.env}-ec2-health_check_failure"
  alarm_description   = "EC2 instances that have failed the Status check."
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = "1"
  evaluation_periods  = "1"
  metric_name         = "StatusCheckFailed"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Maximum"
  dimensions          = { InstanceId = aws_instance.main.id }

  ok_actions = [aws_sns_topic.cloudwatch_alerts_topic.arn]
  alarm_actions = [
    aws_sns_topic.cloudwatch_alerts_topic.arn,
    "arn:aws:automate:${local.config.region}:ec2:reboot"
  ]
  insufficient_data_actions = [aws_sns_topic.cloudwatch_alerts_topic.arn]

  tags = local.tags
}

resource "aws_cloudwatch_metric_alarm" "ec2_high_cpu_utilization" {
  count               = local.config.env != "dev" ? 1 : 0
  alarm_name          = "${local.config.env}-ec2-high_cpu_utilization"
  alarm_description   = "EC2 instances with high CPU utilization"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  threshold           = "60"
  evaluation_periods  = "5"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "60"
  statistic           = "Average"
  dimensions          = { InstanceId = aws_instance.main.id }

  ok_actions = [aws_sns_topic.cloudwatch_alerts_topic.arn]
  alarm_actions = [
    aws_sns_topic.cloudwatch_alerts_topic.arn,
    "arn:aws:automate:${local.config.region}:ec2:reboot"
  ]
  insufficient_data_actions = [aws_sns_topic.cloudwatch_alerts_topic.arn]

  tags = local.tags
}

resource "aws_cloudwatch_metric_alarm" "ebs_disk_usage_alarm_root" {
  count               = local.config.env != "dev" ? 1 : 0
  alarm_name          = "${local.config.env}-ebs-high_disk_usage-root"
  alarm_description   = "Alarm when EBS disk usage exceeds 80%"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  namespace           = "CWAgent"
  metric_name         = "EBSDiskUsagePercentage"
  period              = "60"
  statistic           = "Average"
  threshold           = "80"

  dimensions = {
    host   = split(".", aws_instance.main.private_dns)[0]
    device = "nvme0n1p1"
    fstype = "ext4"
    path   = "/"
  }

  ok_actions                = [aws_sns_topic.cloudwatch_alerts_topic.arn]
  alarm_actions             = [aws_sns_topic.cloudwatch_alerts_topic.arn]
  insufficient_data_actions = [aws_sns_topic.cloudwatch_alerts_topic.arn]

  tags = local.tags
}

