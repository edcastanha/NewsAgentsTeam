output "sns_topic_arn" {
  description = "O ARN do tópico SNS"
  value       = aws_sns_topic.main.arn
}

output "sns_topic_name" {
  description = "O nome do tópico SNS"
  value       = aws_sns_topic.main.name
}
