# AWS Terraform Modular Infra

This repository contains a **modular Terraform project** to provision basic AWS infrastructure on AWS Cloud:

- VPC
- Subnet
- Security Group
- Network Interface (ENI)
- EC2 instance with Nginx installed

The setup is **fully modular, simple, and variable-driven** using `terraform.tfvars`.

---

## Project Workflow (text description)

- `main.tf` calls all modules and passes variables from `variables.tf` / `terraform.tfvars`.
- `terraform.tfvars` contains all environment-specific values (IPs, AZs, names, AMIs, etc.).
- Modules are independent and reusable, each handling a single resource:

1. **VPC Module**
   - Creates a single VPC.
   - Outputs: `vpc_id`.

2. **Subnet Module**
   - Creates a single subnet inside the VPC.
   - Outputs: `subnet_id`.

3. **Security Group Module**
   - Creates a single security group inside the VPC.
   - Supports multiple ingress rules.
   - Outputs: `sg_id`.

4. **Network Interface Module**
   - Creates a network interface in the subnet with specified SGs and private IPs.
   - Outputs: `network_interface_id`.

5. **EC2 Module**
   - Creates a single EC2 instance inside the subnet.
   - Attaches to SG and optional ENI.
   - Outputs: `instance_id`, `public_ip`, `private_ip`.

---

## How It Works

- `main.tf` wires all modules and passes variables from `terraform.tfvars`.
- To change IPs, instance types, AMIs, AZs, or names, edit **only `terraform.tfvars`**.
- Each module is generic, independent, and easy to maintain.
- The setup is simple: one resource per module, no loops, no complex logic.

