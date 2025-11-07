provider "aws" {
  access_key = "<your-access-key>"
  secret_key = "<your-secret-key>"  
  region = var.aws_region
}

# VPC
module "vpc" {
  source     = "./modules/vpc"
  name       = var.project_name
  cidr_block = var.vpc_cidr
}

# Subnet
module "subnet" {
  source    = "./modules/subnet"
  vpc_id    = module.vpc.vpc_id
  cidr_block = var.subnet_cidr
  az        = var.subnet_az
  name      = "${var.project_name}-subnet"
}

# Security Group
module "sg" {
  source = "./modules/security_group"
  name   = var.sg_name
  vpc_id = module.vpc.vpc_id
  ingress_rules = var.sg_ingress_rules
}

# Network Interface
module "eni" {
  source             = "./modules/network_interface"
  subnet_id          = module.subnet.subnet_id
  private_ips        = [var.ec2_private_ip]
  security_group_ids = [module.sg.sg_id]
}

# EC2
module "ec2" {
  source             = "./modules/ec2"
  name               = var.ec2_name
  ami                = var.ec2_ami
  instance_type      = var.ec2_instance_type
  subnet_id          = module.subnet.subnet_id
  security_group_ids = [module.sg.sg_id]
  key_name           = var.ec2_key_name
  user_data          = var.ec2_user_data
}

