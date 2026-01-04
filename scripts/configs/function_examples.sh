#!/bin/bash

# --- 1. Basic Function (No arguments, no explicit return value) ---
# Syntax style: function_name() { ... }
greet() {
    echo "Hello, world!"
    echo "This function performs a simple task and echoes a message."
}

# --- 2. Function with Arguments (Positional parameters $1, $2, etc.) ---
# Calculates the sum of two numbers passed as arguments
add_numbers() {
    # Check if exactly two arguments are provided
    if [ "$#" -ne 2 ]; then
        echo "Error: Two numbers are required."
        return 1
    fi
    # Use arithmetic expansion $((...)) for calculation
    local sum=$(($1 + $2))
    echo "The sum of $1 and $2 is: $sum"
    return 0
}

# --- 3. Function with Return Status (Signals success/failure via exit code 0-255) ---
# Checks if a file exists and returns an exit status
check_file_exists() {
    local filename="$1"
    if [ -e "$filename" ]; then
        echo "File '$filename' exists." >&2 # Output to stderr to keep stdout clean
        return 0 # Success (0)
    else
        echo "File '$filename' not found." >&2 # Output to stderr
        return 1 # Failure (non-zero)
    fi
}

# --- 4. Function Returning Data (Using command substitution to capture stdout) ---
# Generates a simple random password and prints it to stdout
generate_password() {
    # 'tr' deletes unwanted chars from '/dev/urandom', 'fold' sets width, 'head' takes one line
    tr -dc 'A-Za-z0-9!@#%^&*' < /dev/urandom | fold -w 12 | head -n 1
}


# --------------------------------------------------
# Main script execution starts here
# --------------------------------------------------

echo "--- Executing Basic Function ---"
greet
echo ""

echo "--- Executing Function with Arguments ---"
# Call with correct arguments
add_numbers 10 20
# Capture the function's exit status in the special variable $?
echo "The previous function's exit status was: $?"

# Call with incorrect arguments to demonstrate error handling
add_numbers 5
echo "The previous function's exit status was: $?"
echo ""

echo "--- Executing Function with Return Status (File Check) ---"
touch "test_file.txt" # Create a dummy file
check_file_exists "test_file.txt"
echo "Status of check_file_exists: $?"

check_file_exists "non_existent_file.txt"
echo "Status of check_file_exists: $?"
rm "test_file.txt" # Clean up the dummy file
echo ""

echo "--- Executing Function Returning Data ---"
# Capture the standard output of the function into a variable
PASSWORD=$(generate_password)
echo "Generated Password: $PASSWORD"
echo ""
