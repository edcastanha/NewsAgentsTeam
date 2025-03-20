output "vpc_id" {
  value = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "arn" {
  description = "ARN of vpc"
  value       = aws_vpc.main.arn
}