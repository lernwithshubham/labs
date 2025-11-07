# Project info
variable "project_name" {
  type        = string
  description = "Project name"
  default     = "myproject"
}

variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-east-2"
}

# VPC
variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR block"
}

# Subnet
variable "subnet_cidr" {
  type        = string
  description = "Subnet CIDR block"
}

variable "subnet_az" {
  type        = string
  description = "Availability zone for subnet"
}

# Security Group
variable "sg_name" {
  type        = string
  description = "Security Group name"
}

variable "sg_ingress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  description = "List of ingress rules"
}

# EC2
variable "ec2_name" {
  type        = string
  description = "EC2 instance name"
}

variable "ec2_ami" {
  type        = string
  description = "EC2 AMI ID"
}

variable "ec2_instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "ec2_key_name" {
  type        = string
  description = "SSH key name"
}

variable "ec2_private_ip" {
  type        = string
  description = "Private IP for EC2 / ENI"
}

variable "ec2_user_data" {
  type        = string
  description = "User data script for EC2"
  default     = ""
}

