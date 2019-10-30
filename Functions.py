import Variables as var
import ApplicationSetup
from ApplicationSetup import *
import time
import GPSDATA as gpd

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
    var.combinedMeasurements = open(var.comfilename, "a+")

    print("Started logging")
    var.combinedMeasurements.write("Measurement from:" + var.now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    var.combinedMeasurements.write("Time" + ";" + "Current 1" + ";" + "Current 2" + ";" + "Current 3" + ";" + "Current 4" + ";" + "Velocity 1" + ";" + "Velocity 2" + ";" + "Velocity 3" + ";" + "Velocity 4" + ";" + "Heading" + ";" + "fieldX" + ";" + "fieldY" + ";" + "Latitude" + ";" + "Longitude" + ";" + "LinearSpeed" + ";" + "gx" + ";" + "gy" + ";" + "gz" + ";" + "ax" + ";" + "ay" + ";" + "az" + ";" +"\n")
    var.logging = True



def stopLogging():
    print("Stopped logging")
    var.logging = False

def logging(imu):
    try:
        var.combinedMeasurements.write(
        str(time.time()) + ";" + str(var.motCur[0]) + ";" + str(var.motCur[1]) + ";" + str(var.motCur[2]) + ";" + str(var.motCur[3]) + ";" + str(var.motVel[0]) + ";" + str(var.motVel[1]) + ";" + str(var.motVel[2]) + ";" + str(var.motVel[3]) + ";" + str(var.MagnetometerLogging.heading) + ";" + str(var.MagnetometerLogging.fieldX) + ";" + str(var.MagnetometerLogging.fieldY) + ";" + str(var.GPSLogging.latitude) + ";" + str(var.GPSLogging.longitude) + ";" + str(var.GPSLogging.linear_speed) + ";" + str(imu.gx) + ";" + str(imu.gy) + ";" + str(imu.gz) + ";" + str(imu.ax) + ";" + str(imu.ay) + ";" + str(imu.az) + "\n")
    except Exception as e:
        print(e)
