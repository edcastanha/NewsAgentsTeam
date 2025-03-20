output "rds_endpoint" {
  description = "O endpoint do RDS"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "rds_arn" {
  description = "O ARN do RDS"
  value       = aws_db_instance.main.arn
}

output "rds_name" {
  description = "O nome do RDS"
  value       = aws_db_instance.main.name
}
