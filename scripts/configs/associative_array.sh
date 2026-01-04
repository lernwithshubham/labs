#!/bin/bash
# --- Associative Array Example ---
echo -e "\n--- Associative Array Example ---"

# Declare an associative array (the 'declare -A' is mandatory)
declare -A user_details

# Add key-value pairs
user_details[name]="John Doe"
user_details[email]="john@example.com"
user_details[age]=30
user_details[role]="Developer"

# Access and print values using string keys
echo "User's name: ${user_details[name]}"
echo "User's role: ${user_details[role]}"

# Print all values
echo "All details: ${user_details[@]}"
echo "