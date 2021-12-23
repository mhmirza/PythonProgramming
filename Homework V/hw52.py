#Homework 5, Part 2
#Authors: Mohammad Manzoor Hassan Mirza, mmmirza
#Sanjana Parmar, sparmar2

#Q2 to #Q5)

from sensor import Sensor
from alarm import Alarm

# Display the sensor-alarm menu, get valid choice
def menu():
    print('1. Display sensors')
    print('2. Display alarms')
    print('3. Change sensor')
    print('4. Quit')
    choice = int(input('Enter your choice: '))
    if choice < 1 or choice > 4:
         choice = 4 # Quit if the user is stupid
    return choice

# Create and return a list of sensors and a list of alarms
def init():
    sensors = [Sensor('Kitchen', 300.0), Sensor('Bedroom', 150.0)]
    alarms = [Alarm('Kitchen'), Alarm ('Bedroom')]                                #Q2)
    return sensors, alarms

# Sound all alarms
def soundAlarms(alarms):                                                          #Q3)
    for i in alarms:
        i.soundAlarm()

# Initialize the sensors and alarms
# Get a menu choice
# Perform that choice
# Repeat until done
def main():
    sensorList, alarmList = init()

    choice = menu()
    while choice != 4:
        # Display the sensors
        if choice == 1:
            print()
            print('Sensor list:')
            count = 0
            for s in sensorList:
                print(str(count) + ': ' + s.__str__())
                count += 1
            print()
        # Display the alarms
        elif choice == 2:                                                         #Q4)
            print()
            count = 0
            for i in alarmList:
                print(str(count) + ': ' + i.__str__())
                count += 1
            print()
            
        # Test by changing one sensor and see if the
        #   sensor trips; if so, sound all alarms
        elif choice == 3:
            sensorNumber = int(input('Enter the sensor number: '))
            if sensorNumber < 0 or sensorNumber > len(sensorList):
                print('Error, bad sensor number')
            else:
                print('Current value = ' + str(sensorList[sensorNumber].getValue()) )
                value = float(input('Enter new value: '))
                sensorList[sensorNumber].setValue(value)
                print(sensorList[sensorNumber].getValue())
                for i in sensorList:                                              #Q5)
                    if i.trip():
                        soundAlarms(alarmList)
                        i.reset()

        choice = menu()

if __name__ == '__main__':
    main()
