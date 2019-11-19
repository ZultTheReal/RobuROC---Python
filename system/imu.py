import serial
import time
from .shared import *

class IMU:
    
    # Sensors class reads data from custom pcb with IMU and ultrasonic sensors
    
    connected = False
    data = [0,0,0,0,0,0]
    
    def __init__(self):
        self.gx = 0          # Number of connected satellites
        self.gy = 0          # timestamp
        self.gz = 0           # lateral coordinate
        self.ax = 0       # lateral direction (North,South)
        self.ay = 0          # Longitudinal coordinate
        self.az = 0      # Longitudinal direction (West,East)
        self.dfront = 0
        self.dback = 0
        
    def connect(self,comPort):
        try:
            self.ser = serial.Serial(
                port= comPort,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.05
            )
            self.connected = True
        except Exception as error:
            self.connected = False
            errors.append( ['Sensor', 'Not connected'] )
        
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
                    
                    if strlen == 8:
                        
                        data = dict(item.split('=') for item in packlist)
                        
                        self.gx = float(data["gx"])
                        self.gy = float(data["gy"])
                        self.gz = float(data["gz"])
                        self.ax = float(data["ax"])
                        self.ay = float(data["ay"])
                        self.az = float(data["az"])
                        self.dfront = float(data["d1"])
                        self.dback = float(data["d2"])
                        
                        self.data[0] = self.gx
                        self.data[1] = self.gy
                        self.data[2] = self.gz
                        self.data[3] = self.ax
                        self.data[4] = self.ay
                        self.data[5] = self.az
    
                except Exception as error:
                    errors.append( ['Sensors', 'Failed to translate string'] )
