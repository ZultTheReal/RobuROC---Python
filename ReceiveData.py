import Variables
from Variables import *

def readData(canid, data, timestamp):
    scaled = 0
    value = abs(int.from_bytes(data, byteorder='little', signed=True))
    print(logging)

    if (canid in curCanID):
        scaled = value/Variables.currentScaling
        motindex = int(curCanID.index(canid))
        motCur[motindex] = scaled
        print(str(motindex) + " : " + str(motCur[motindex]))
        if logging:
            currentmeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(scaled) + " [A]" + "\n")

    if (canid in posCanID):
        scaled = value
        if logging:
            postionmeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(scaled) + " [P]" + "\n")

def startPeriodic():
    print("Starting periodic messages")

    #RTR - Actual Current
    for i in range(0, 4):
        curSig[i] = network.send_periodic(897 + i, 8, .1, remote=True)
        network.subscribe(897 + i, readData)

    #RTR - Actual Position
    for i in range(0, 4):
        posSig[i] = network.send_periodic(913 + i, 8, .1, remote=True)
        network.subscribe(913 + i, readData)

def stopPeriodic():
    print("Stop periodic messages")
    currentmeasurements.close()
    postionmeasurements.close()

    for i in range(0, 4):
        posSig[i].stop()
        curSig[i].stop()