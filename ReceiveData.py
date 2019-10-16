import canopen
import Functions
from Functions import *
import Variables
from Variables import *

def readData(canid, data, timestamp):

    scaled = 0
    value = abs(int.from_bytes(data, byteorder='little', signed=True))

    if (canid in curCanID):
        scaled = value/currentScaling
        currentmeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(scaled) + " [A]" + "\n")

    if (canid in posCanID):
        scaled = value
        postionmeasurements.write(str(timestamp) + ";" + str(canid) + ";" + str(scaled) + " [P]" + "\n")

def startPeriodic(self):
    print("Starting periodic messages")
    currentmeasurements.write("Measurement from:" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    currentmeasurements.write("Timestamp" + ";" + "CANID" + ";" + "Data [A]" + "\n\n")
    postionmeasurements.write("Measurement from:" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")
    postionmeasurements.write("Timestamp" + ";" + "CANID" + ";" + "Data [P]" + "\n\n")

    #RTR - Actual Current
    for i in range(0, 4):
        curSig[i] = network.send_periodic(897 + i, 8, .1, remote=True)
        network.subscribe(897 + i, readData)

    #RTR - Actual Position
    for i in range(0, 4):
        posSig[i] = network.send_periodic(913 + i, 8, .1, remote=True)
        network.subscribe(913 + i, readData)

def stopPeriodic(self):
    print("Stop periodic messages")
    currentmeasurements.close()

    for i in range(0, 4):
        posSig[i].stop()
        curSig[i].stop()