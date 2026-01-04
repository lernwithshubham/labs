#!/bin/bash

# Define a variable for testing
NUMBER=$1

# Check if a command-line argument was provided
if [ -z "$NUMBER" ]; then
    echo "Error: Please provide a number as a command-line argument."
    echo "Usage: ./script_name.sh <number>"
    exit 1
fi

# --- IF/ELIF/ELSE Ladder ---
# The script checks the range of the number using an if-elif-else ladder.

if [[ "$NUMBER" -gt 100 ]]; then
    echo "$NUMBER is greater than 100."
elif [[ "$NUMBER" -gt 50 ]]; then
    echo "$NUMBER is between 51 and 100 (inclusive)."
elif [[ "$NUMBER" -gt 10 ]]; then
    # --- NESTED IF Statement ---
    # This block is executed only if the number is greater than 10.
    echo "$NUMBER is between 11 and 50 (inclusive). Checking for odd/even..."

    # Nested check: determine if the number is even or odd
    if [[ $((NUMBER % 2)) -eq 0 ]]; then
        echo "  Nested Result: $NUMBER is an even number."
    else
        echo "  Nested Result: $NUMBER is an odd number."
    fi
    # End of nested if statement (fi)

else
    echo "$NUMBER is 10 or less."
fi

# The 'fi' keyword marks the end of the initial if/elif/else structure.
