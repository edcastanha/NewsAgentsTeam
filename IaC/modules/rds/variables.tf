variable "db_subnet_group_name" {
  description = "O nome do grupo de subnets do RDS"
  type        = string
  default     = "meu-grupo-subnet-rds"
}

variable "subnet_ids" {
  description = "Os IDs das subnets onde o RDS será criado"
  type        = list(string)
}

variable "allocated_storage" {
  description = "O armazenamento alocado para o RDS (em GB)"
  type        = number
  default     = 20
}

variable "engine" {
  description = "O tipo de engine do banco de dados (ex: mysql, postgres, etc.)"
  type        = string
  default     = "mysql"
}

variable "engine_version" {
  description = "A versão da engine do banco de dados"
  type        = string
  default     = "8.0.33"
}

variable "instance_class" {
  description = "O tipo de instância do RDS (ex: db.t3.micro, db.t3.small, etc.)"
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "O nome do banco de dados"
  type        = string
}

variable "db_username" {
  description = "O nome de usuário do banco de dados"
  type        = string
  default = "admin"
}

variable "db_password" {
  description = "A senha do banco de dados"
  type        = string
  sensitive   = true
  default = "testdbpass"
}

variable "skip_final_snapshot" {
  description = "Se deve pular o snapshot final ao deletar o RDS"
  type        = bool
  default     = true
}

variable "vpc_security_group_ids" {
  description = "Os IDs dos security groups para o RDS"
  type        = list(string)
}

variable "identifier" {
  description = "O identificador da instancia do banco de dados"
  type        = string
  default     = "news-db-rds"
}
