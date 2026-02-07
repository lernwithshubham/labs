provider "aws" {
  region = "us-east-1"
}

# FIX 1: Make Bucket Private
resource "aws_s3_bucket" "data_bucket" {
  bucket = "demo-company-data-bucket"
  acl    = "private"  # Changed from public-read
}

# FIX 2: Restrict SSH to Internal Network
resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    description = "SSH from Internal VPN"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]  # Changed from 0.0.0.0/0
  }
}