import serial
import pynmea2

magfail = 1

class Magnetometer:
    def __init__(self):
        self.heading         = 0
        self.pitch           = 0
        self.roll            = 0
        self.wat             = 0
        self.accelerometerX  = 0
        self.accelerometerY  = 0
        self.accelerometerZ  = 0
        self.msg = 1
    def __str__(self):
        return f'Heading: {self.heading}   Pitch: {self.pitch}   Roll: {self.roll}   wat: {self.wat}   Acceleration X: {self.accelerometerX}   Acceleration Y: {self.accelerometerY}   Acceleration Z: {self.accelerometerZ} '

def GetMagnetometerData():
    obj = Magnetometer()
    num = ser.in_waiting
    if num != 0:
        try:
            line = ser.readline()
            line = str(line)
            temp = line.split()
            magnetoData = temp[1].split(",")
            obj.msg = 1
            obj.heading = magnetoData[0]
            obj.pitch = magnetoData[1]
            obj.roll = magnetoData[2]
            obj.wat = magnetoData[3]
            obj.accelerometerX = magnetoData[4]
            obj.accelerometerY = magnetoData[5]
            obj.accelerometerZ = magnetoData[6]

        except:
            print("Error in Magnometer")
            magfail = 0
            return

        return obj
    else:
        return 0

ser = serial.Serial(
    port='COM4',\
    baudrate=19200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)



