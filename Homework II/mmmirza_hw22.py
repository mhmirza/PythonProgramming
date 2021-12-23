#Author: Mohammad Manzoor Hassan Mirza, mmmirza
#Homework 2 - Part 2, 90819-A2

#Problem 2)
print ('\nQ2)\n')

import pandas as pd

allPop = pd.read_csv ('nstData.csv')

#a)
print ('\nQ2a)\n')

print (allPop.head(2), '\n')

print (allPop.tail(5), '\n')

#b)
print ('\nQ2b)\n')

print (allPop.describe(), '\n')

print (allPop ["ESTIMATESBASE2010"].describe(), '\n')

print ('Mean for 2010 base estimate: {:,.2f}'.format (allPop ["ESTIMATESBASE2010"].mean(), '\n'))

#c)
print ('\nQ2c)\n')

states = allPop ["NAME"]
states = states [5:]
print (states, '\n')

#d)
print ('\nQ2d)\n')

row_constraint = allPop ["STATE"] != 0
states2 = allPop.loc [row_constraint, "NAME"]
print (states2, '\n')

print (states == states2)

#e)
print ('\nQ2e)\n')

myPop = allPop.copy() #STEP 0

myPop = myPop [["REGION", "STATE", "NAME", "POPESTIMATE2010"]]  #STEP 1

myPop = myPop.loc [allPop ["STATE"] != 0] #STEP 2

myPop.rename (columns = {"POPESTIMATE2010": "POPULATION"}, inplace = True) #STEP 3

myPop.loc [myPop ["NAME"] == "Puerto Rico", "REGION"] = 5 #STEP 4

myPop["REGION"] = pd.to_numeric (myPop ["REGION"]) #STEP 5

print (myPop ["REGION"].dtypes) #testing the updated data type of region column

myPop.reset_index (drop = True, inplace = True)

pop = pd.read_csv('pop.csv')

print (myPop, '\n')

print (myPop == pop)
