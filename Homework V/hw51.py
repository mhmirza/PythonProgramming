#Homework 5, Part 1
#Author: Mohammad Manzoor Hassan Mirza, mmmirza
#Sanjana Parmar, sparmar2

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Q1)
print ('\nQuestion 1)\n')

weather = pd.read_csv ('weather5.csv')
print (weather, '\n')

print ('Column names of weather: {}\n'.format(weather.columns.values))

print ('Number of columns in weather: {}\n'.format(len (weather.loc[0])))  

print ('Number of rows in weather: {}\n'.format(len (weather['Temperature']))) #+1 for header

weather.dropna (inplace = True)

print ('Number of rows in updated weather: {}\n'.format(len (weather['Temperature']))) #+1 for header

#function takes one parameter and resets its value to 100 if the para is greater than 100 or resets the value to 0 if parameter is less than 0
def filter (para):
    if para > 100:
        return 100
    elif para < 0:
        return 0
    else:
        return para

weather['Humidity'] = weather['Humidity'].apply(filter)

print (weather, '\n')

#Q2)
print ('\nQuestion 2)\n')

#function takes a string parameter (time in 24h format) and returns two strings i.e. first is time converted to 12 hour format, second is AM or PM

def toTime (time):
    vals = time.split (':')
    if int (vals [0]) < 12:
        vals [0] = time
        vals [1] = 'AM'
    elif int (vals [0]) == 12:
        vals [0] = time
        vals [1] = 'PM'
    else:
        vals [0] = str((int (vals [0]) - 12)) + ':' + vals [1]
        vals [1] = 'PM'
    return vals [0], vals [1]


AM_PM = []
HH_MM = []

for i in weather['Time'].values:
    a, b = toTime (i)
    AM_PM.append(b)
    HH_MM.append(a)

weather ['12Hour'] = HH_MM
weather ['AM-PM'] = AM_PM

print ('{0:<7}{1:<7}{2:<7}{3:<12}{4:<10}{5:<7}{6:<15}'.format(weather.columns [0], weather.columns [5], weather.columns [6], weather.columns [1],
                                                            weather.columns [2], weather.columns [3], weather.columns [4]))
for i in weather.index:
    print ('{0:<7}{1:<7}{2:<7}{3:<12}{4:<10}{5:<7}{6:<15}'.format(weather['Time'].loc[i], weather['12Hour'].loc[i], weather['AM-PM'].loc[i],
                                                                weather['Temperature'].loc[i], weather['Humidity'].loc[i], weather['Wind'].loc[i],
                                                                weather['Clouds'].loc[i]))

#Q3)
print ('\nQuestion 3)\n')

#function takes a string parameter (time 24h format) and returns the time in minutes since midnight
def toMinutes(time):
    vals = time.split (':')
    elapsed = int (vals [0]) * 60 + int (vals [1])
    return elapsed

weather['Elapsed'] = weather['Time'].apply(toMinutes)

print ('{0:<7}{1:<7}{2:<7}{3:<10}{4:<12}{5:<10}{5:<9}{6:<15}'.format(weather.columns [0], weather.columns [5], weather.columns [6], weather.columns [7],
                                                                     weather.columns [1], weather.columns [2], weather.columns [3], weather.columns [4]))
for i in weather.index:
    print ('{0:<7}{1:<7}{2:<7}{3:<10}{4:<12}{4:<10}{5:<9}{6:<15}'.format(weather['Time'].loc[i], weather['12Hour'].loc[i], weather['AM-PM'].loc[i],
                                                                         weather['Elapsed'].loc[i], weather['Temperature'].loc[i],
                                                                         weather['Humidity'].loc[i], weather['Wind'].loc[i], weather['Clouds'].loc[i])) 
#Q4)
plt.title('Temperature Data')
cols = weather.columns
plt.xlabel(cols[7])
plt.ylabel(cols[1])
plt.scatter(weather['Elapsed'], weather['Temperature'], color = 'blue')
plt.show()

#Q5)
plt.title('Humidity Data')
cols = weather.columns
plt.xlabel(cols[7])
plt.ylabel(cols[2])
plt.plot(weather['Elapsed'], weather['Humidity'], color = 'black')
plt.show()

#Q6)
plt.title('Wind')
plt.xlabel(cols[3])
plt.ylabel('Frequency')
plt.hist(weather['Wind'], bins=5)
plt.show()

#Q7)
plt.title('Temperature Data')
plt.xlabel(cols[7])
plt.ylabel(cols[1])
plt.ylim(ymin = 0, ymax = weather['Temperature'].max() + 1)
plt.scatter(weather['Elapsed'], weather['Temperature'], color = 'blue')
plt.show()

#Q8)
c = round(weather['Temperature'].corr(weather['Humidity']), 2)
s = str(c)
plt.title('Temperature x Humidity, Correlation = ' + s)
sns.regplot(x = 'Temperature', y = 'Humidity', data = weather)
plt.show()

#Q9)
sns.relplot(x = 'Elapsed', y = 'Temperature', col = 'AM-PM', size = 'Temperature', sizes = (20, 200), data = weather)
plt.show()

sns.relplot(x = 'Elapsed', y = 'Temperature', col = 'Clouds', size = 'Temperature', sizes = (20, 200), data = weather)
plt.show()

#Q10)
sns.factorplot(x = "Clouds", y = "Temperature", kind = 'bar', col = 'AM-PM', data = weather)
plt.show()

sns.factorplot(x = "Clouds", y = "Temperature", kind = 'box', col = 'AM-PM', data = weather)
plt.show()
