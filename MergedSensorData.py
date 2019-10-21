import serial
import pynmea2

class GPS:
    def __init__(self):
        self.sat_count = 0          # Number of connected satellites
        self.timestamp = 0          # timestamp
        self.latitude = 0           # lateral coordinate
        self.latitude_dir = 0       # lateral direction (North,South)
        self.longitude = 0          # Longitudinal coordinate
        self.longitude_dir = 0      # Longitudinal direction (West,East)
        self.heading = 0            # Which direction the vehicle is heading
        self.linear_speed = 0
        self.rate_of_climb = 0      # Vertical speed (uphill)
    def __str__(self):
        return f'Satellite Count: {self.sat_count}   Timestamp: {self.timestamp}  Latitude: {self.latitude}   Latitude Direction: {self.latitude_dir}   Longitude: {self.longitude}   Longitude Direction: {self.longitude_dir}   Heading: {self.heading}   Linear_speed: {self.linear_speed}'

class Magnetometer:
    def __init__(self):
        self.heading         = 0
        self.pitch           = 0
        self.roll            = 0
        self.wat             = 0
        self.accelerometerX  = 0
        self.accelerometerY  = 0
        self.accelerometerZ  = 0
    def __str__(self):
        return f'Heading: {self.heading}   Pitch: {self.pitch}   Roll: {self.roll}   wat: {self.wat}   Acceleration X: {self.accelerometerX}   acceleration Y: {self.accelerometerY}   Acceleration Z: {self.accelerometerZ} '

GPSSerial = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0)

MagnetometerSerial = serial.Serial(
    port='COM4',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0)

print("GPS connected to: " + GPSSerial.portstr)
print("Magnetometer connected to: " + MagnetometerSerial.portstr)

def getGPSData():
    obj = GPS()
    num = GPSSerial.in_waiting
    if num != 0:
        line = GPSSerial.readline()
        string = str(line)
        string = string.replace("b'", " ")
        string = string.replace("\\r\\n'", "")
        temp = string.split(",")
        stringlen = len(temp)
        if stringlen == 19:
            try:
                msg = pynmea2.parse(string)
                obj.sat_count = msg.sat_count
                obj.timestamp = msg.timestamp
                obj.latitude = msg.lat
                obj.latitude_dir = msg.lat_dir
                obj.longitude = msg.lon
                obj.longitude_dir = msg.lon_dir
                obj.heading = msg.course
                obj.linear_speed = msg.spd_over_grnd
                return obj
            except:
                print("Error in NMEA IDE")
                return 0
        else:
            return 0
    else:
        return 0

def GetMagnetometerData():
    obj = Magnetometer()
    num = MagnetometerSerial.in_waiting
    if num != 0:
        try:
            line = MagnetometerSerial.readline()
            line = str(line)
            temp = line.split()
            magnetoData = temp[1].split(",")
            obj.heading = magnetoData[0]
            obj.pitch = magnetoData[1]
            obj.roll = magnetoData[2]
            obj.wat = magnetoData[3]
            obj.accelerometerX = magnetoData[4]
            obj.accelerometerY = magnetoData[5]
            obj.accelerometerZ = magnetoData[6]
            return obj

        except:
            print("Error in Magnometer")
            return 0

    else:
        return 0

while 1:
    GPSData = getGPSData()
    MagnetometerData = GetMagnetometerData()
    if GPSData != 0:
        print(GPSData)
        print("\n")
    if MagnetometerData != 0:
        print(MagnetometerData)
        print("\n")
