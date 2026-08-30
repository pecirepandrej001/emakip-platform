data "aws_vpc" "default" { default = true }
resource "aws_db_subnet_group" "this" {
  name       = "${var.project_name}-db-subnets"
  subnet_ids = data.aws_subnets.default.ids
}
data "aws_subnets" "default" {
  filter { name = "vpc-id"; values = [data.aws_vpc.default.id] }
}
resource "aws_db_instance" "this" {
  identifier             = "${var.project_name}-postgres"
  engine                 = "postgres"
  engine_version         = "17"
  instance_class         = "db.t4g.micro"
  allocated_storage      = 20
  username               = "emakip"
  password               = var.db_password
  db_name                = "emakip"
  db_subnet_group_name   = aws_db_subnet_group.this.name
  skip_final_snapshot    = true
  publicly_accessible    = false
  storage_encrypted      = true
}
