import Variables
from Variables import *
import ApplicationSetup
from ApplicationSetup import *

def velocityArray( value ):
    data = [15, 0]
    tempSpeed = (value).to_bytes(4, byteorder="little", signed=True)
    return data + list(tempSpeed)

def checkMotorSpeed(speed):
    if speed > 5200000:
        print("This value is above the speedlimit, please enter a value below: 5200000")
    else:
        print("The motorspeed is now set to:", speed)
        Variables.globalspeed = speed

def setSpeed():
    tempId = int(ApplicationSetup.motor.get())
    motorSpeed[tempId] = int(ApplicationSetup.speed.get())

def startLogging():
    print("Started logging")
    currentmeasurements.write("Measurement from:" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    currentmeasurements.write("Timestamp" + ";" + "CANID" + ";" + "Data [A]" + "\n\n")
    postionmeasurements.write("Measurement from:" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    postionmeasurements.write("Timestamp" + ";" + "CANID" + ";" + "Data [P]" + "\n\n")
    logging = True
    print(logging)

def stopLogging():
    print("Stopped logging")
    currentmeasurements.close()
    postionmeasurements.close()
    logging = False
    print(logging)