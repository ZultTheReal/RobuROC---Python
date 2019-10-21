import time
import ApplicationSetup as apps
import Variables as var
import Functions as f
from joystick import Joystick
import GPSDATA as gsd
import MagnometerData as msd
import ReceiveData as rd

gamepad = Joystick()

# Variables for gampepad control
lastGamepad = 0
left = 0
right = 0

rd.startPeriodic()


def updateTelemetry():
    apps.cur1Label['text'] = str(round( var.motCur[0], 2)) + " A"
    apps.cur2Label['text'] = str(round( var.motCur[1], 2)) + " A"
    apps.cur3Label['text'] = str(round( var.motCur[2], 2)) + " A"
    apps.cur4Label['text'] = str(round( var.motCur[3], 2)) + " A"

    apps.vel1Label['text'] = str(round( var.motVel[0], 2)) + " m/s"
    apps.vel2Label['text'] = str(round( var.motVel[1], 2)) + " m/s"
    apps.vel3Label['text'] = str(round( var.motVel[2], 2)) + " m/s"
    apps.vel4Label['text'] = str(round( var.motVel[3], 2)) + " m/s"



while(var.appOpen):
    updateTelemetry()
    apps.app.update()

    GPSData = gsd.getGPSData()
    MagnetometerData = msd.GetMagnetometerData()

    if GPSData != 0:
        #print(GPSData)
        if var.logging:
            var.positionMeasurements.write(str(GPSData.sat_count) + ";" + str(GPSData.timestamp) + ";" + str(GPSData.latitude) + ";" + str(GPSData.latitude_dir) + ";" + str(GPSData.longitude) + ";" + str(GPSData.longitude_dir) + ";" + str(GPSData.heading) + ";" + str(GPSData.linear_speed) + "\n")

    if MagnetometerData != 0:
        #print(MagnetometerData)
        if var.logging:
            var.directionMeasurements.write(str(MagnetometerData.heading) + ";" + str(MagnetometerData.pitch) + ";" + str(MagnetometerData.roll) + ";" + str(MagnetometerData.wat) + ";" + str(MagnetometerData.accelerometerX) + ";" + str(MagnetometerData.accelerometerY) + ";" + str(MagnetometerData.accelerometerZ) + "\n")

    
    # Not connected to gamepad, try to reconnect
    if not gamepad.connected:
        gamepad.connect()
 
 
    if( time.time() - lastGamepad > 0.1 ):
        
        # Listen for gamepad events
        gamepad.run()
        
        lastSpeed = time.time()
        
        # Calculate left and right speeds
        left = round(gamepad.getForward() + gamepad.getRotate()/4, 2)
        right = -round(gamepad.getForward() - gamepad.getRotate()/4, 2)
        
        
        for i in range(4):
            
            if( i % 2) == 0:
                var.motorSpeed[i] = int(left * var.maxSpeed)
            else:
                var.motorSpeed[i] = int(right * var.maxSpeed)
            
            #print( "canReady: " + str( var.driveReady) )
            if( var.driveReady == True):
                var.network.send_message(var.addressMap[i], f.velocityArray(var.motorSpeed[i]), remote=False )
    