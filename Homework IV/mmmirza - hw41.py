#Author: Mohammad Manzoor Hassan Mirza
#Homework 41


import re

#Part 1) 
print ('\nPart 1)\n')

with open ('pop.csv', 'r') as fin:
    states = []
    for line in fin:
        states.append (line [:-1])
    print (states, '\n')

patterns = [r'Oregon', r'O', r'[OP]', r'^1', r'0$', r'[s-zS-Z]', r'[0][0]*', r'^[^34]*5[^3]*4[^5]*3[^45]*', r'[A-Za-z]+ [A-Za-z]+', r'[iI].*[iI]+']

ques = 0
for p in patterns:
    print ('\n')
    ques += 1
    for string in states:
        if re.search (p, string) != None:
            print ('{}: Pattern {} matches string {}'.format(ques, p, string))


