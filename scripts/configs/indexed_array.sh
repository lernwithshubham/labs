#!/bin/bash

# --- Indexed Array Example ---
echo "--- Indexed Array Example ---"

# Declare and initialize an indexed array (explicit declare -a is optional)
indexed_array=("Apple" "Banana" "Orange" "Grape")

# Add a new element using compound assignment
indexed_array+=("Mango")

# Access and print elements using numerical indices (starting from 0)
echo "First element: ${indexed_array[0]}"
echo "Third element: ${indexed_array[2]}"
echo "Last element: ${indexed_array[-1]}"

# Print all elements
echo "All elements: ${indexed_array[@]}"
