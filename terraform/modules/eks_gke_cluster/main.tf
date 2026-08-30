resource "aws_eks_cluster" "this" {
  name     = "${var.project_name}-eks"
  role_arn = aws_iam_role.cluster.arn
  vpc_config { subnet_ids = data.aws_subnets.default.ids }
}
data "aws_vpc" "default" { default = true }
data "aws_subnets" "default" { filter { name = "vpc-id"; values = [data.aws_vpc.default.id] } }
resource "aws_iam_role" "cluster" {
  name = "${var.project_name}-eks-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{Effect="Allow", Principal={Service="eks.amazonaws.com"}, Action="sts:AssumeRole"}]
  })
}
resource "aws_iam_role_policy_attachment" "cluster" {
  role = aws_iam_role.cluster.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}
output "cluster_name" { value = aws_eks_cluster.this.name }
