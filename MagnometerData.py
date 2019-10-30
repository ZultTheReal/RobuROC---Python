import serial
import pynmea2

magfail = 1

class Magnetometer:
    def __init__(self):
        self.heading         = 0
        self.fieldX           = 0
        self.fieldY            = 0
        self.fieldZ             = 0
        self.accelerometerX  = 0
        self.accelerometerY  = 0
        self.accelerometerZ  = 0
        self.msg = 1
    def __str__(self):
        return f'Heading: {self.heading}   Pitch: {self.fieldX}   Roll: {self.fieldY}   wat: {self.fieldZ}   Acceleration X: {self.accelerometerX}   Acceleration Y: {self.accelerometerY}   Acceleration Z: {self.accelerometerZ} '

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
            obj.fieldX = magnetoData[1]
            obj.fieldY = magnetoData[2]
            obj.fieldZ = magnetoData[3]
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

try:
    ser = serial.Serial(
        port='COM6',\
        baudrate=19200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
    print("connected to: " + ser.portstr)
except:
    print("Magnometer cannot connect")




