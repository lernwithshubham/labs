project_name = "myproject"
aws_region   = "us-east-2"

vpc_cidr     = "10.0.0.0/16"
subnet_cidr  = "10.0.1.0/24"
subnet_az    = "us-east-2b"

sg_name = "web-sg"
sg_ingress_rules = [
  { from_port = 22, to_port = 22, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] },
  { from_port = 80, to_port = 80, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] },
  { from_port = 443, to_port = 443, protocol = "tcp", cidr_blocks = ["0.0.0.0/0"] }
]

ec2_name          = "web-server"
ec2_ami           = "ami-0c5ddb3560e768732"
ec2_instance_type = "t2.micro"
ec2_key_name      = "<your-key>"
ec2_private_ip    = "10.0.1.10"
ec2_user_data     = <<-EOT
  #!/bin/bash
  sudo apt update -y
  sudo apt install -y nginx
  sudo systemctl enable nginx
  sudo systemctl start nginx
EOT

