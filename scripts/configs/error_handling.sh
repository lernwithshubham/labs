#!/bin/bash

# --- Runtime Error Handling with 'set -e' and 'trap' ---

# Define an error handling function that logs the error with line number and exits
handle_error() {
    local parent_lineno="$1"
    local message="$2"
    echo "❌ ERROR on line ${parent_lineno}: ${message}; exiting." >&2
    exit 1
}

# Use trap to call handle_error function whenever a command exits with a non-zero status (ERR signal)
trap 'handle_error ${LINENO} "$BASH_COMMAND"' ERR

# set -e: Exit immediately if any command fails. This ensures subsequent commands are not executed.
set -e

echo "Starting a safe backup operation..."

# This command should succeed
mkdir -p /tmp/my_backup_dir 

# Example of a command that will fail (runtime error)
# This will trigger the 'trap' and exit the script
cp /nonexistent_source_file.txt /tmp/my_backup_dir/

# This line will NOT be reached if the 'cp' command fails
echo "✅ Backup operation finished successfully!" 
