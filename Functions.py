import Variables as var
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
        var.globalspeed = speed

def setSpeed():
    tempId = int(ApplicationSetup.motor.get())
    var.motorSpeed[tempId] = int(ApplicationSetup.speed.get())

def startLogging():
    var.currentMeasurements = open(var.curfilename, "a+")
    var.postionMeasurements = open(var.posfilename, "a+")
    print("Started logging")
    var.currentMeasurements.write("Measurement from:" + var.now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    var.currentMeasurements.write("Timestamp" + ";" + "CANID" + ";" + "Data [A]" + "\n\n")
    var.postionMeasurements.write("Measurement from:" + var.now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    var.postionMeasurements.write("Timestamp" + ";" + "CANID" + ";" + "Data [P]" + "\n\n")
    var.logging = True
    print(var.logging)

def stopLogging():
    print("Stopped logging")
    var.currentMeasurements.close()
    var.postionMeasurements.close()
    var.logging = False
    print(var.logging)