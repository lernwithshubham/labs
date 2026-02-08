package kubernetes.validating

import rego.v1

# Rule 1: Block 'latest' image tags
deny contains msg if {
  # Find all containers in the input
  container := input.spec.template.spec.containers[_]
  
  # Check if image ends with ':latest'
  endswith(container.image, ":latest")
  
  # Define the error message
  msg := sprintf("Security Risk: Container '%v' uses the ':latest' tag. Use a specific version.", [container.name])
}

# Rule 2: Enforce High Availability (Min 3 Replicas)
deny contains msg if {
  input.kind == "Deployment"
  input.spec.replicas < 3
  
  msg := sprintf("Reliability Risk: Deployment has %v replicas. Minimum required is 3.", [input.spec.replicas])
}
