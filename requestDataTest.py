import time
import canopen

# Initiate the canopen object
network = canopen.Network()

# Connect to the PCAN adapter
network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)

# Reset and enable all four drives
for i in range(4):
    # Reset
    network.send_message(0, [0x81, i])
    time.sleep(0.2)
    # Enable
    network.send_message(0, [0x1, i])
    
    

def readData(canid, data, timestamp):
    print( str(canid) + ":" + str( int.from_bytes(data, byteorder='little', signed=True)))


periodicPos = [None, None, None, None]


for i in range(0,4):
    # Request data from drives with a period of 0.1s
    periodicPos[i] = network.send_periodic(897+i, 8, 1, remote=True)
    # Enable callback to read incoming messages for specific CAN-ids
    network.subscribe( 897+i, readData );

#time.sleep(5)

#print("Stopping")

#for i in range(0,4):
 #   periodicPos[i].stop()
