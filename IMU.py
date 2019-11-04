import serial
import time

class IMU:
    def __init__(self):
        self.gx = 0          # Number of connected satellites
        self.gy = 0          # timestamp
        self.gz = 0           # lateral coordinate
        self.ax = 0       # lateral direction (North,South)
        self.ay = 0          # Longitudinal coordinate
        self.az = 0      # Longitudinal direction (West,East)
    def __str__(self):
        return f'gx: {self.gx}   gy: {self.gy}  gz: {self.gz}   ax: {self.ax}   ay: {self.ay}   az: {self.az}'


try:
    ser = serial.Serial(
        port='COM11',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5)
    print("IMU connected to: " + ser.portstr)
except:
    print("IMU was not able to connect")

def getIMUData():
    obj = IMU()
    if ser.in_waiting != 0:
        while ser.in_waiting !=0:
            data = ser.readline()
        try:
            string = str(data,"utf-8")
            packlist = string.split(',')
            strlen = len(packlist)
            if strlen == 6:
                imuData = dict(item.split('=') for item in packlist)
                obj.gx = float(imuData["gx"])
                obj.gy = float(imuData["gy"])
                obj.gz = float(imuData["gz"])
                obj.ax = float(imuData["ax"])
                obj.ay = float(imuData["ay"])
                obj.az = float(imuData["az"])
                return obj
        except:
            return -1
    else:
        return -1



#A = IMU()

# while (1):
#     A = getIMUData()
#     print(A)
#     time.sleep(50/1000)
    