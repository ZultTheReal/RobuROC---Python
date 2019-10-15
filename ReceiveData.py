import canopen

def readData(canid, data, timestamp):
    print( str(canid) + ":" + str( int.from_bytes(data, byteorder='little', signed=True)))

def startPeriodic(self):
    print("Starting periodic messages")
    # RTR - Live Signal Drives
    #    for i in range(0, 4):
    #        liveSig[0] = network.send_periodic(1793 + i, 8, .1, remote=True)
    #        network.subscribe(1793 + i, fc.readData)

    #RTR - Actual Current
    # for i in range(0, 4):
    #     curSig[i] = network.send_periodic(897 + i, 8, .1, remote=True)
    #     network.subscribe(897 + i, fc.readData)

    #RTR - Actual Position
    # for i in range(0, 4):
    #     posSig[0] = network.send_periodic(913 + i, 8, .1, remote=True)
    #     network.subscribe(913 + i, fc.readData)

def stopPeriodic(self):
    print("Stop periodic messages")

    # for i in range(0, 4):
    #     posSig[i].stop()
    #     curSig[i].stop()
    #     liveSig[i].stop()