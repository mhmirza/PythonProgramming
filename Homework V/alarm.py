#Homework 5, Part 2
#Authors: Mohammad Manzoor Hassan Mirza, mmmirza
#Sanjana Parmar, sparmar2

#Q1)

class Alarm:
    def __init__(self, location):   #hardcoding message, hence not required to set it as a parameter    
        self._location = location
        self._message = 'Warning! Warning!'

    def getLocation(self):        #getter for the data member i.e. location
        return self._location

    def soundAlarm(self):
        print(self._message + ', ' + self._location)

    def __str__(self):                #returns the message and location as one string
        return self._message + ', ' + self._location

    



    
