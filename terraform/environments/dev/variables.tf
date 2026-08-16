variable "project_name" {
  description = "Project name"
  type        = string
  default     = "customer-churn"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "key_name" {
  description = "Existing EC2 key pair"
  type        = string
  default     = "micro"
}

variable "ami_id" {
  description = "Ubuntu 24.04 AMI"
  type        = string
  default     = "ami-07e5ce642bbc48c0d"
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
  default     = "vpc-05f69601439ec1d9d"
}

variable "subnet_id" {
  description = "Public subnet ID"
  type        = string
  default     = "subnet-0dc4bd43fb3e4588e"
}
