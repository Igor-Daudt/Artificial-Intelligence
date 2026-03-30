#!/bin/zsh

python autograder.py -q q1 > q1.autotemp 
python autograder.py -q q2 > q2.autotemp 
python autograder.py -q q3 > q3.autotemp 
python autograder.py -q q4 > q4.autotemp 
python autograder.py -q q5 > q5.autotemp 
python autograder.py -q q6 > q6.autotemp 
python autograder.py -q q7 > q7.autotemp 
python autograder.py -q q8 > q8.autotemp

cat *.autotemp | grep Total: 

rm *.autotemp
