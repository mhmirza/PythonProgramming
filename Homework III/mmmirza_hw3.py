#Mohammad Manzoor Hassan Mirza
#Homework 3

import pandas as pd
import sqlite3

#Problem 1)
print ('\nProblem 1)\n')

with open ('JustLeeBooks.txt', 'r') as f:
    commands = []
    for line in f:
        line = line [:-1]
        if len (line) > 0:
            commands.append (line)

print (commands)

#Problem 2)        

connection = sqlite3.connect ('LeeBooks.db')

cursor = connection.cursor()

for c in commands:
    cursor.execute (c)
connection.commit()

#Problem 3)
print ('\nProblem 3)\n')

#getting table names from the database
query = 'SELECT name FROM sqlite_master WHERE type = "table"'

cursor.execute (query)   
tbl_names = cursor.fetchall()  

#the outer for loop iterates through every tuple in tbl_names (a list of tuples), prints it's 0th item & then executes a query to pull column names for that table
#the nested for loop iterates through col_names (a list of tuples) of the specific table currently run by the outer loop, and prints the 1st element of every tuple  

for row in tbl_names:
    print ('Table: {}'.format (row [0]))
    query = 'PRAGMA table_info(' + row[0] + ')'
    cursor.execute(query)
    col_names = cursor.fetchall()
    print('Columns: |', end = ' ')
    for row in col_names:
        print (row [1], end = " | ")
    print ('\n')

#Problem 4)  
print ('\nProblem 4)\n')

query = 'SELECT LASTNAME, FIRSTNAME, STATE FROM CUSTOMERS'
cursor.execute (query)
table = cursor.fetchall()

customersDF = pd.DataFrame (table, columns = [name[0] for name in cursor.description])

print (customersDF, '\n')

print (customersDF.sort_values (by = 'STATE'), '\n') #dataframe sorted by state

print (customersDF.sort_values (by = ['STATE', 'LASTNAME']), '\n')   #dataframe sorted by two columns

#Problem 5)
print ('\nProblem 5)\n')

query = 'SELECT ORDERNUM, QUANTITY, PAIDEACH FROM ORDERITEMS'
cursor.execute (query)
table = cursor.fetchall()

orderItemsDF = pd.DataFrame (table, columns =  [name[0] for name in cursor.description])

orderItemsDF ['TOTAL'] = orderItemsDF ['QUANTITY'] * orderItemsDF ['PAIDEACH']

print (orderItemsDF, '\n')

print ('Overall Total: ${:,.0f}'.format (orderItemsDF ['TOTAL'].sum()))

#Problem 6) 
print ('\nProblem 6)\n')

query = '''CREATE TABLE BOOKLIST AS
SELECT A.LNAME AS AUTHOR_LASTNAME, A.FNAME AS AUTHOR_FIRSTNAME, B.TITLE AS BOOK_TITLE
FROM BOOKS B JOIN BOOKAUTHOR BA USING (ISBN)
JOIN AUTHOR A USING (AUTHORID)'''

cursor.execute(query)
connection.commit()

query = 'SELECT * FROM BOOKLIST'
cursor.execute (query)
table = cursor.fetchall()

for rows in table:
    print (rows)

#Problem 7) 
print ('\nProblem 7)\n')

bookListDF = pd.DataFrame (table, columns =  [name[0] for name in cursor.description])
print (bookListDF, '\n')

print (bookListDF.sort_values (by = ['AUTHOR_LASTNAME', 'AUTHOR_FIRSTNAME']), '\n')

print (bookListDF.groupby ('AUTHOR_LASTNAME')[['AUTHOR_FIRSTNAME', 'BOOK_TITLE']].count(), '\n')

#Response: The result of the JOINS used to create the booklist table in the database results in repitition of author's firstname and lastname...
#...This is in cases where one author has written more than one book, hence the count of entries after grouping by author's lastname counts repeating rows...
#Moreover, since LISA & WILLIAM both have the same lastname i.e. WHITE, grouping by lastname counts rows for these 2 together instead of displaying each's count

#Problem 8) 

query = 'SELECT name FROM sqlite_master WHERE type = "table"'

cursor.execute (query)   
tbl_names = cursor.fetchall()

for row in tbl_names:
    print ('Table: {}'.format (row [0]))
    query = 'PRAGMA table_info(' + row[0] + ')'
    cursor.execute(query)
    col_names = cursor.fetchall()
    query = 'SELECT * FROM(' + row[0] + ')'
    cursor.execute(query)
    rows = cursor.fetchall()
    print('Columns: |', end = ' ')
    for row in col_names:
        print (row [1], end = " | ")
    print ('\n# Rows = {}\n'.format (len (rows)))
