import time
import ApplicationSetup as apps
import Variables as var
import Functions as f
from xbox360_gamepad import Gamepad, XboxMap
import GPSDATA as gsd
import MagnometerData as msd
import ReceiveData as rd
import IMU as imu

gamepad = Gamepad()

lastlog = 0

# Variables for gampepad control
lastGamepad = 0
left = 0
right = 0

rd.startPeriodic()


def updateTelemetry():
    apps.cur1Label['text'] = str(round(var.motCur[0], 2)) + " A"
    apps.cur2Label['text'] = str(round(var.motCur[1], 2)) + " A"
    apps.cur3Label['text'] = str(round(var.motCur[2], 2)) + " A"
    apps.cur4Label['text'] = str(round(var.motCur[3], 2)) + " A"

    apps.vel1Label['text'] = str(round(var.motVel[0], 2)) + " m/s"
    apps.vel2Label['text'] = str(round(var.motVel[1], 2)) + " m/s"
    apps.vel3Label['text'] = str(round(var.motVel[2], 2)) + " m/s"
    apps.vel4Label['text'] = str(round(var.motVel[3], 2)) + " m/s"

    apps.pos1Label['text'] = str(round(var.motPos[0], 2)) + " m"
    apps.pos2Label['text'] = str(round(var.motPos[1], 2)) + " m"
    apps.pos3Label['text'] = str(round(var.motPos[2], 2)) + " m"
    apps.pos4Label['text'] = str(round(var.motPos[3], 2)) + " m"


while (var.appOpen):
    updateTelemetry()
    apps.app.update()

    GPSData = gsd.getGPSData()

    MagnetometerData = msd.GetMagnetometerData()

    IMUData = imu.getIMUData()

    if GPSData != 0:
        #print(GPSData)
        var.GPSLogging = GPSData

    if MagnetometerData != 0:
        var.MagnetometerLogging = MagnetometerData

    if IMUData != 0 and IMUData is not None:
        #print(IMUData.gx)
        var.IMULogging = IMUData

    if var.logging:

        if time.time() - var.lastlog > 1:
            var.lastlog = time.time()
            f.logging(IMUData)

    if time.time() - lastGamepad > .1:
        # Get all button states
        pressed = gamepad.buttons()
        # Get joystick values
        joystick = gamepad.left_stick()

        # print( joystick )

        lastGamepad = time.time()

        # Calculate left and right speeds
        left = round(joystick[XboxMap.yAxis] + joystick[XboxMap.xAxis] / 4, 2)
        right = -round(joystick[XboxMap.yAxis] - joystick[XboxMap.xAxis] / 4, 2)

        for i in range(4):

            if (i % 2) == 0:
                var.motorSpeed[i] = int(left * var.maxSpeed)
            else:
                var.motorSpeed[i] = int(right * var.maxSpeed)

            # print( "canReady: " + str( var.driveReady) )
            if (var.driveReady == True):
                var.network.send_message(var.addressMap[i], f.velocityArray(var.motorSpeed[i]), remote=False)
