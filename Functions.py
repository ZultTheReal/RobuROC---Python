import Variables as var
import ApplicationSetup
from ApplicationSetup import *
import GPSDATA

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


def startLogging():
    var.currentMeasurements = open(var.curfilename, "a+")
    var.velocityMeasurements = open(var.velfilename, "a+")
    var.positionMeasurements = open(var.posfilename, "a+")
    var.directionMeasurements = open(var.dirfilename, "a+")

    print("Started logging")
    var.currentMeasurements.write("Measurement from:" + var.now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    var.currentMeasurements.write("Timestamp" + ";" + "CANID" + ";" + "Current [A]" + "\n\n")
    var.velocityMeasurements.write("Measurement from:" + var.now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    var.velocityMeasurements.write("Timestamp" + ";" + "CANID" + ";" + "Velocity [V]" + "\n\n")
    var.positionMeasurements.write("Measurement from:" + var.now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    var.positionMeasurements.write("Sat. Count" + ";" + "Timestamp" + ";" + "Latitude" + ";" + "Latitude Dir" + ";" + "Longitude" + ";" + "Longitude Dir" + ";" + "Heading" + ";" + "Linear speed" + "\n\n")
    var.directionMeasurements.write("Measurement from:" + var.now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    var.directionMeasurements.write("Heading" + ";" + "Pitch" + ";" + "Roll" + ";" + "wat" + ";" + "Acceleration X" + ";" + "Acceleration Y" + ";" + "Acceleration Z" + "\n\n")
    var.logging = True

def stopLogging():
    print("Stopped logging")
    var.logging = False
    var.currentMeasurements.close()
    var.velocityMeasurements.close()
    var.positionMeasurements.close()
    var.directionMeasurements.close()