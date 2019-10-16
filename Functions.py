import MainWindow
import Variables
from MainWindow import *
import MovementCommands
from MovementCommands import *

def velocityArray(value):
    data = [0x0F, 0]
    tempSpeed = int(value).to_bytes(4, byteorder="little", signed=True)
    return data + list(tempSpeed)

def checkMotorSpeed(speed):

    if speed > 5200000:
        print("This value is above the speedlimit, please enter a value below: 5200000")

    else:
        print("The motorspeed is now set to:", speed)
        Variables.globalspeed = speed

def convert_manualspeed(temptextinput):
    converttext = temptextinput
    if len(converttext) > 0:  # if text is not empty
        print(format(converttext))
        checkMotorSpeed(int(converttext))
    else:
        print("Error: Empty string")
