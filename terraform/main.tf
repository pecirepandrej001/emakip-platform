terraform {
  required_version = ">= 1.8"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.aws_region
}

module "cluster" {
  source       = "./modules/eks_gke_cluster"
  project_name = var.project_name
}

module "postgres" {
  source       = "./modules/postgres_db"
  project_name = var.project_name
  db_password  = var.db_password
}

module "vector_database" {
  source       = "./modules/vector_database"
  project_name = var.project_name
}
