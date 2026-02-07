package kubernetes.validating

# Deny if image uses :latest tag
deny[msg] {
  container := input.spec.template.spec.containers[_]
  endswith(container.image, ":latest")
  msg := sprintf("Container '%v' uses ':latest' image. Pin a specific version.", [container.name])
}

# Deny if replicas are less than 3
deny[msg] {
  input.kind == "Deployment"
  input.spec.replicas < 3
  msg := "Replica count is too low. Production requires at least 3."
}