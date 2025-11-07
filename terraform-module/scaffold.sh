#!/usr/bin/env bash

project="$1"

if [ -z "$project" ]; then
  echo "Usage: ./scaffold.sh <project-name>"
  exit 1
fi

mkdir -p "${project}"
cd "${project}"

touch main.tf variables.tf outputs.tf

mkdir -p modules/vpc
touch modules/vpc/main.tf modules/vpc/variables.tf modules/vpc/outputs.tf

mkdir -p modules/subnet
touch modules/subnet/main.tf modules/subnet/variables.tf modules/subnet/outputs.tf

mkdir -p modules/security_group
touch modules/security_group/main.tf modules/security_group/variables.tf modules/security_group/outputs.tf

mkdir -p modules/network_interface
touch modules/network_interface/main.tf modules/network_interface/variables.tf modules/network_interface/outputs.tf

mkdir -p modules/ec2
touch modules/ec2/main.tf modules/ec2/variables.tf modules/ec2/outputs.tf

echo "structure created under ${project}/"

