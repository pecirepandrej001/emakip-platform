output "cluster_name" { value = module.cluster.cluster_name }
output "postgres_endpoint" { value = module.postgres.endpoint }
output "qdrant_namespace" { value = module.vector_database.namespace }
