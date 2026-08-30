resource "aws_cloudwatch_log_group" "qdrant" {
  name              = "/emakip/${var.project_name}/qdrant"
  retention_in_days = 30
}
