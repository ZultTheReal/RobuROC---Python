import Variables as var
from Functions import *

def readData(canid, data, timestamp):

    scaled = 0
    value = abs(int.from_bytes(data, byteorder='little', signed=True))
    # print(var.logging)

    if canid in var.curCanID:
        scaled = value/var.currentScaling
        motindex = int(var.curCanID.index(canid))
        var.motCur[motindex] = scaled
        #print(str(motindex) + " : " + str(var.motCur[motindex]))
        #if var.logging:
        #    var.currentMeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(scaled) + " [A]" + "\n")

    if canid in var.posCanID:
        scaled = value * var.positionScaling
        motindex = int(var.posCanID.index(canid))
        var.motPos[motindex] = scaled
        #print(str(motindex) + " : " + str(var.motPos[motindex]))
        #if var.logging:
        #    var.motPositionMeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(scaled) + " [m]" + "\n")

    if canid in var.velCanID:
        velscaled = value * var.velocityScaling
        motindex = int(var.velCanID.index(canid))
        var.motVel[motindex] = velscaled
        #print(str(motindex) + " : " + str(var.motVel[motindex]))
        #if var.logging:
        #    var.velocityMeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(velscaled) + " [m/s]" + "\n")

def startPeriodic():
    print("Starting periodic messages")

    #RTR - Actual Current
    for i in range(0, 4):
        var.curSig[i] = var.network.send_periodic(var.curCanID[i], 8, .1, remote=True)
        var.network.subscribe(var.curCanID[i], readData)

    #RTR - Actual Position
    for i in range(0, 4):
        var.posSig[i] = var.network.send_periodic(var.posCanID[i], 8, .1, remote=True)
        var.network.subscribe(var.posCanID[i], readData)

    #RTR - Actual Velocity
    for i in range(0, 4):
        var.velSig[i] = var.network.send_periodic(var.velCanID[i], 8, .1, remote=True)
        var.network.subscribe(var.velCanID[i], readData)


def stopPeriodic():
    print("Stop periodic messages")

    for i in range(0, 4):
        var.posSig[i].stop()
        var.curSig[i].stop()
        var.velSig[i].stop()