# cost.py

import sys
import ast  # Import Abstract Syntax Tree library

def calculate_total():
    user_input = sys.argv[1]
    
    try:
        # FIX: literal_eval strictly parses data. 
        # It creates a python object but REFUSES to execute functions.
        data = ast.literal_eval(user_input)
        print(f"Total Cost: ${sum(data)}")
    except Exception:
        # If an attack is detected, we catch the error safely.
        print("Error: Security violation or invalid input!")

if __name__ == "__main__":
    calculate_total()
