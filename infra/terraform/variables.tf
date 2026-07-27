variable "aws_region" {
  description = "AWS region to deploy the VM into."
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Prefix used for naming AWS resources."
  type        = string
  default     = "patent-app"
}

variable "instance_type" {
  description = "EC2 instance size."
  type        = string
  default     = "t3.micro"
}

variable "app_repo_url" {
  description = "GitHub repository URL that contains this project."
  type        = string
}

variable "app_branch" {
  description = "Git branch to deploy from."
  type        = string
  default     = "main"
}

variable "key_name" {
  description = "EC2 key pair name for SSH access."
  type        = string
  default     = "demo-project"
}

variable "private_key_output_path" {
  description = "Local path where Terraform writes the generated private key PEM file."
  type        = string
  default     = "demo-project.pem"
}

variable "vpc_cidr" {
  description = "CIDR block for the custom VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "root_volume_size" {
  description = "Root EBS volume size for the EC2 instance in GiB."
  type        = number
  default     = 10
}
