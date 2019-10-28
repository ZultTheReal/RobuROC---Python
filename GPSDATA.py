import serial
import pynmea2
import time

gpsfail = 1

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
        self.msg = 1
    def __str__(self):
        return f'Satellite Count: {self.sat_count}   Timestamp: {self.timestamp}  Latitude: {self.latitude}   Latitude Direction: {self.latitude_dir}   Longitude: {self.longitude}   Longitude Direction: {self.longitude_dir}   Heading: {self.heading}   Linear_speed: {self.linear_speed}'


ser = serial.Serial(
    port='COM8',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0)

print("GPS connected to: " + ser.portstr)

def getGPSData():
    obj = GPS()
    num = ser.in_waiting
    if num != 0:
        line = ser.readline()
        string = str(line)
        string = string.replace("b'", " ")
        string = string.replace("\\r\\n'", "")
        temp = string.split(",")
        stringlen = len(temp)
        if stringlen == 19:
            try:
                msg = pynmea2.parse(string)
                obj.msg = 1
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
                #print("Error in NMEA IDE")
                gpsfail = 0
                return 0
        else:
            return 0
    else:
        return 0
