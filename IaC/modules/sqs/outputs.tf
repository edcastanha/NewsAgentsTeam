output "sqs_queue_arn" {
  description = "O ARN da fila SQS"
  value       = aws_sqs_queue.main.arn
}

output "sqs_queue_url" {
  description = "A URL da fila SQS"
  value       = aws_sqs_queue.main.id
}

output "sqs_queue_name" {
  description = "O nome da fila SQS"
  value       = aws_sqs_queue.main.name
}
