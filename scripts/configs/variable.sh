#!/bin/bash

: << 'EOF'
your multi-line comment
goes here
nothing in this block will run
EOF

<<COMMENT
testing
abc
wijtsw
COMMENT

abc=123 #declaring variable

echo $abc #printing local variable
echo $PWD #printing environment variable
echo "Welcome to variable script"

#printing special variables
echo "script name" $0:
echo "total number of arguments" $#:
echo "prints arguments passed" $@:
echo "processID for this execution" $$:

#string concatenation
a="Weclome"
b=" Session"
var=${a}${b}
echo $a$b
echo $var

#substring extraction
string='Hello,World!'
substring=${string:7:5}
echo $substring

