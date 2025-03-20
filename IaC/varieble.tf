variable "instance_type" {
  description = "The type of EC2 instance to use."
  type        = string
  default     = "t2.micro"
}

variable "key_name" {
  description = "The key name of the AWS Key Pair to be used for the EC2 instance."
  type        = string
  default     = "my-key-pair"
}

variable "ami_id" {
  description = "The AMI ID to be used for the EC2 instance."
  type        = string
  default     = "ami-0f29c8402f8cce65c"
}

variable "public_key" {
  description = "The public key to be used for the AWS Key Pair."
  type        = string
  default     = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDZ6"
}

variable "region" {
  description = "The region in which the resources will be created."
  type        = string
  default     = "sa-east-1"

}

variable "access_key" {
  description = "The access key to be used to authenticate with AWS."
  type        = string
  default     = "testeNews"
}

variable "secret_key" {
  description = "value of secret key"
  type        = string
  default     = "testeNews"
}

variable "public_subnet_id" {
  description = "The ID of the public subnet."
  type        = string
  default = "subnet-0f29c8402f8cce65c"
}

variable "db_password" {
  description = "A senha do banco de dados"
  type        = string
  sensitive   = true
  default = "NewsKeystore"
}


variable "db_name" {
  description = "O nome do banco de dados"
  type        = string
  default = "news_db"
  sensitive   = true

}

variable "db_user" {
  description = "O nome do usuario do banco de dados"
  type        = string
  default = "news_user"
  sensitive   = true

}
