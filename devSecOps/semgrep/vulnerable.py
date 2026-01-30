# cost.py

import sys

def calculate_total():
    # sys.argv[1] is like "$1" in Bash (the first command line argument)
    user_input = sys.argv[1]
    
    # VULNERABILITY: eval() executes the input string as Python Code.
    # If the user inputs a list "[10, 20]", it works.
    # If the user inputs a command, it runs the command.
    data = eval(user_input)
    
    print(f"Total Cost: ${sum(data)}")

if __name__ == "__main__":
    calculate_total()
