import time
import Variables
from Variables import *

def enable():
    # Enable all drives with global NMT command
    # Reset command: 0x01
    print("Enabling Drives")
    for i in range(4):
        network.send_message(0, [0x1, i])

def quickStop():
    # Transitions the drives into quick stop state with a PDO message
    # Quick Stop command: 0x02
    print("Set to QuickStop State")
    quickStop = [0x02, 0]
    for i in range(4):
        network.send_message(addressMap[i], quickStop, remote=False)

def reset():
    # Reset all drives with global NMT command
    # Reset command: 0x81
    print("Resetting the Drives")
    for i in range(4):
        network.send_message(0, [0x81, i])
        print("network.send_message(0, ", [0x81, i], ")")
        time.sleep(.2)

def disableVoltage():
    # Disable all drives with PDO message
    # To disable the voltage the drive must be in quick stop state
    # Disable Voltage command: 0x00
    print("Set to DisableVoltage State")
    disVoltage = [0x0, 0]
    for i in range(4):
        network.send_message(addressMap[i], disVoltage, remote=False)

def shutDown():
    # Shutdown the drives with a PDO message
    # Shutdown command: 0x06
    print("Set to ShutDown State")
    data = [0x06, 0]
    for i in range(4):
        print(i)
        network.send_message(addressMap[i], data, remote=False)