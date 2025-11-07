variable "vpc_id" {
  type        = string
  description = "VPC ID where subnet will be created"
}

variable "cidr_block" {
  type        = string
  description = "Subnet CIDR block"
}

variable "az" {
  type        = string
  description = "Availability Zone"
}

variable "name" {
  type        = string
  description = "Subnet name"
}

variable "tags" {
  type    = map(string)
  default = {}
}

