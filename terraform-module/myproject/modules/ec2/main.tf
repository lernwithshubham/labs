resource "aws_instance" "this" {
  ami                    = var.ami
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.security_group_ids
  key_name               = var.key_name
  private_ip             = var.private_ip
  associate_public_ip_address = true
  user_data              = var.user_data
  tags                   = merge(var.tags, { Name = var.name })
}

