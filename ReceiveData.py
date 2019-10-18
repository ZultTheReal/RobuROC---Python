import Variables as var
from Functions import *

def readData(canid, data, timestamp):
    scaled = 0
    value = abs(int.from_bytes(data, byteorder='little', signed=True))
    print(var.logging)

    if (canid in var.curCanID):
        scaled = value/var.currentScaling
        motindex = int(var.curCanID.index(canid))
        var.motCur[motindex] = scaled
        print(str(motindex) + " : " + str(var.motCur[motindex]))
        if var.logging:
            var.currentMeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(scaled) + " [A]" + "\n")

    if (canid in var.posCanID):
        scaled = value
        if var.logging:
            var.postionMeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(scaled) + " [P]" + "\n")

def startPeriodic():
    print("Starting periodic messages")

    #RTR - Actual Current
    for i in range(0, 4):
        var.curSig[i] = var.network.send_periodic(897 + i, 8, .1, remote=True)
        var.network.subscribe(897 + i, readData)

    #RTR - Actual Position
    for i in range(0, 4):
        var.posSig[i] = var.network.send_periodic(913 + i, 8, .1, remote=True)
        var.network.subscribe(913 + i, readData)

def stopPeriodic():
    print("Stop periodic messages")
    var.currentMeasurements.close()
    var.postionMeasurements.close()

    for i in range(0, 4):
        var.posSig[i].stop()
        var.curSig[i].stop()