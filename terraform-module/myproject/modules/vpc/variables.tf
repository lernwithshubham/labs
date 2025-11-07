variable "name" {
  type        = string
  description = "VPC name"
}

variable "cidr_block" {
  type        = string
  description = "CIDR block for the VPC"
}

variable "tags" {
  type    = map(string)
  default = {}
}

