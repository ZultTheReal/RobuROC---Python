import serial
import time
from .shared import *

class IMU:
    
    connected = False
    data = [0,0,0,0,0,0]
    
    def __init__(self):
        self.gx = 0          # Number of connected satellites
        self.gy = 0          # timestamp
        self.gz = 0           # lateral coordinate
        self.ax = 0       # lateral direction (North,South)
        self.ay = 0          # Longitudinal coordinate
        self.az = 0      # Longitudinal direction (West,East)
        
    def __str__(self):
        return f'gx: {self.gx}   gy: {self.gy}  gz: {self.gz}   ax: {self.ax}   ay: {self.ay}   az: {self.az}'


    def connect(self,comPort):
        try:
            self.ser = serial.Serial(
                port= comPort,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.5
            )

            var.imuConnected = True

            return 0
        
        except Exception as error:
            
            var.imuConnected = False
            return -1
        
    def getData(self):

        try:
            bytesWaiting = self.ser.in_waiting
            self.connected = True
        except Exception as error:
            self.connected = False

        if self.connected:
            
            tempString = ''
            while self.ser.in_waiting !=0:
                tempString = self.ser.readline()
                
                
            # Every line from buffer is read, now use the newest to get data
            if tempString != '':
                try:
                   
                    string = str(tempString,"utf-8").strip('\r\n')
                    
                    packlist = string.split(',')
                    strlen = len(packlist)
                    
                    if strlen == 6:
                        imuData = dict(item.split('=') for item in packlist)
                        self.gx = float(imuData["gx"])
                        self.gy = float(imuData["gy"])
                        self.gz = float(imuData["gz"])
                        self.ax = float(imuData["ax"])
                        self.ay = float(imuData["ay"])
                        self.az = float(imuData["az"])
                        
                        self.data[0] = self.gx
                        self.data[1] = self.gy
                        self.data[2] = self.gz
                        self.data[3] = self.ax
                        self.data[4] = self.ay
                        self.data[5] = self.az
                        
                        return 0
                except:
                    return -1