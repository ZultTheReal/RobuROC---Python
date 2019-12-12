import serial
import time
import math
from .shared import *

class IMU:
    
    # Sensors class reads data from custom pcb with IMU and ultrasonic sensors
    gyroDeadzone = 0.5 # deg/s
    connected = False
    data = [0,0,0]
    
    def __init__(self):
        self.gx = 0          # Number of connected satellites
        self.gy = 0          # timestamp
        self.gz = 0           # lateral coordinate
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
                timeout=0.01
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
                    
                    if strlen == 5:
                        
                        data = dict(item.split('=') for item in packlist)
                        
                        gx = float(data["gx"])
                        gy = float(data["gy"])
                        gz = float(data["gz"])
                        
                        gx = gx if abs(gx) > self.gyroDeadzone else 0.0
                        gy = gy if abs(gy) > self.gyroDeadzone else 0.0
                        gz = gz if abs(gz) > self.gyroDeadzone else 0.0
                        
                        self.gx = gx * math.pi/180.0 # Convert deg/s to rad/s
                        self.gy = gy * math.pi/180.0 # Convert deg/s to rad/s
                        self.gz = gz * math.pi/180.0 # Convert deg/s to rad/s
                        # self.ax = float(data["ax"])
                        # self.ay = float(data["ay"])
                        # self.az = float(data["az"])
                        self.dfront = float(data["d1"])
                        self.dback = float(data["d2"])
                        
                        #print(self.gz)
                        
                        self.data[0] = self.gx
                        self.data[1] = self.gy
                        self.data[2] = self.gz
    
                except Exception as error:
                    errors.append( ['Sensors', 'Failed to translate string'] )
