#!/bin/bash
set -e

APP_NAME="StripePaymentProcessor"
SECRET_NAME="prod/stripe/apikey"

echo "----------------------------------------"
echo "Starting $APP_NAME Deployment..."
echo "----------------------------------------"

# 1. Fetch the secret at runtime
# We use --query to extract just the text value so we don't get JSON formatting
echo "[INFO] Fetching credentials from Vault..."
API_KEY=$(aws secretsmanager get-secret-value \
    --secret-id $SECRET_NAME \
    --query SecretString \
    --output text)

# 2. Validate the secret
if [ -z "$API_KEY" ]; then
    echo "[ERROR] Failed to retrieve API Key. Aborting!"
    exit 1
fi

# 3. Simulate usage (WITH MASKING)
# CRITICAL: Never print full secrets to console logs.
# We take the first 7 characters and mask the rest.
MASKED_KEY="${API_KEY:0:7}****************"

echo "[INFO] Authenticating with Payment Gateway..."
echo "[INFO] Using Key: $MASKED_KEY"

# Simulate a process
sleep 2
echo "[SUCCESS] Connection established. Payment Service is Live."
echo "----------------------------------------"