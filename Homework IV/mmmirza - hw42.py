#Author: Mohammad Manzoor Hassan Mirza
#Homework 42

import pandas as pd
import json
import requests

#Part 2)

#the function takes in a topic, queries the google books API and returns a dataframe with title and author columns for the relevant books

def BookInfo (topic):
    headers = {'Content-Type': 'application/json'}
    url = 'https://www.googleapis.com/books/v1/volumes?q=topic:' + t  #Ques 1
    response = requests.get(url, headers = headers)
    if response.status_code == 200:
        thedict = json.loads(response.content.decode('utf-8'))   #Ques 2
        df = pd.json_normalize (thedict['items'])
        subset_df = df [['volumeInfo.title', 'volumeInfo.authors']].copy()    #Ques 3
        subset_df.rename (columns = {"volumeInfo.title": "Title", "volumeInfo.authors": "Authors"}, inplace = True)  #Ques 4
    return subset_df


topics = ['Python', 'Data Science', 'Data Analysis', 'Machine Learning', 'Deep Learning'] #a list of topics which will serve as an input to the BookInfo function 
dataframes = [] #create an empty list used to capture the dataframes returned by the for loop below for each topic 

for t in topics:
    subset_df = BookInfo (t)  #the for loop yields five dataframe objects, one for each topic/iteration by calling the function BookInfo
    dataframes.append (subset_df)   #stores all dataframe objects in a list called dataframes
    
bigTable = pd.concat (dataframes, ignore_index = True)   #creates a big table concatenating dataframes i.e. a list
print (bigTable, '\n') #Ques 5

print ('{0:<30}{1:<30}'.format(bigTable.columns [0], bigTable.columns [1][:6]))
for i in bigTable.index:
    if type(bigTable['Authors'].iloc[i]) is float:
        print ('{0:<30}{1:<30}'.format(bigTable['Title'].iloc[i][:25], 'Not Available'))
    else:
        print ('{0:<30}{1:<30}'.format(bigTable['Title'].iloc[i][:25], bigTable['Authors'].iloc[i][0]))  #Ques 6
