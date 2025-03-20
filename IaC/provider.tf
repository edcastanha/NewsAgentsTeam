provider "aws" {
  region     = var.region
  secret_key = var.secret_key
  access_key = var.access_key
  endpoints {
    ec2            = "http://localhost:4566"
    s3             = "http://localhost:4566"
    sts            = "http://localhost:4566"
    cloudformation = "http://localhost:4566"
    lambda         = "http://localhost:4566"
    sns            = "http://localhost:4566"
    sqs            = "http://localhost:4566"
  }
}