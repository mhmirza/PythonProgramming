#Author: Mohammad Manzoor Hassan Mirza, mmmirza
#Homework 2 - Part 1, 90819-A2

#Problem 1)
print ('\nQ1)\n')

import pandas as pd


#the menu function presentes 7 options to the user to choose from, prompts the user to enter a number corresponding to an action
#returns a valid int b/w 0-6 if the user enters a number between 0-6, else prints an error message

def menu():
    menu_options = {1: "Display the entire table",
                    2: "Display the total population of all the states",
                    3: "Prompt for the name of a state. Display its population",
                    4: "Display the table sorted by state name",
                    5: "Display the table grouped by region",
                    6: "Display the table sorted by population, largest to smallest",
                    0: "Quit"}
    print ('\n{0:<15}{1:<62}'.format ("Number Choice", "Action to Perform"))
    for i in menu_options:
        print ('{0:<15}{1:<62}'.format (i, menu_options [i]))
    entry = int (input ("\nEnter a number to choose from the menu displayed above: "))
    return (entry)

#the main function opens the file, loops until the menu() function returns 0
#performing a specific action for each valid int 0-6 returned by the menu function

def main():
    pop = pd.read_csv ('pop.csv')
    entry = menu()
    while entry != 0:
        if entry == 1:
            print ("\nThe entire table:\n\n", pop)
        elif entry == 2:
            print ("\nThe total population of all the states: {:,}\n".format(pop ["POPULATION"].sum()))
        elif entry == 3:
            state = input ("Enter the name of the state to get population: ")
            if state in pop.values:
                row_constraint = pop["NAME"] == state #returns a boolean vector
                print ("\nThe population of {} is{}.\n".format (state, pop.loc [row_constraint, "POPULATION"].to_string (index = False))) #returns the values from population column and only rows which satisfy boolean cond.
            else:
                print ("State not found!")
        elif entry == 4:
            print ("\nThe table sorted by state name:\n\n", pop.sort_values (by = "NAME"))
        elif entry == 5:
            print ("\nThe table grouped by region:\n\n", pop.sort_values (by = "REGION"))
        elif entry == 6:
            print ("\nThe table sorted by population, largest to smallest:\n\n", pop.sort_values (by = "POPULATION", ascending = False))
        else:
            print ("Error: Please enter a number between 0 to 6 inclusive!")
        entry = menu()
    if entry == 0:
        print ('\nQuit!')
        
if __name__ == '__main__':
    main()   
