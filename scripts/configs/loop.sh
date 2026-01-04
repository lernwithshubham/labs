#!/bin/bash

# --- For Loop Example ---
day="Mon Tue Wed Thu Fri"
for d in $day
do
  echo "day  : $d"
done

# --- While Loop Example ---
value=1

while [ $value -le 5 ]; do
 echo $(($value * 3))            
 value=$(($value+1))
done

# --- Until Loop Example ---
counter=2

until [ "$counter" -le 0 ]; do
  echo "Counter is at $counter"
  counter=$((counter - 1))
done
echo "Loop ended at $counter"

