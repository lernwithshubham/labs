#!/bin/bash

echo -n "Are you a student? [yes or no]: "
read response

case $response in
    "Y" | "y" | "YES" | "Yes" | "yes")
        echo "Yes, I am a student."
        ;;
    "N" | "n" | "NO" | "No" | "no")
        echo "No, I am not a student."
        ;;
    *)
        echo "Invalid input: Please enter yes or no."
        ;;
esac
