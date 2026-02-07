provider "aws" {
  region = "us-east-1"
}

# VULNERABILITY 1: Public S3 Bucket
resource "aws_s3_bucket" "data_bucket" {
  bucket = "demo-company-data-bucket"
  acl    = "public-read"
}

# VULNERABILITY 2: Open SSH Port
resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh"
  description = "Allow SSH inbound traffic"

  ingress {
    description = "SSH from world"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}