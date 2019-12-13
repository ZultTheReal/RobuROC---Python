import serial
import time
import math
from .shared import *

class Compass:
    
    connected = False
    data = [0, 0, 0] # Heading
    
    mx_max = 852.6
    mx_min = -36481.6
    
    my_max = 22031.5
    my_min = -25075.3

    heading = 0
    
    def __init__(self):
        self.mx = 0          # Magnetometer reading in x
        self.my = 0          # Magnetometer reading in y
        self.mz = 0          # Magnetometer reading in z
        
    def connect(self,comPort):
        try:
            self.ser = serial.Serial(
                port= comPort,
                baudrate=19200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.01
            )
            self.connected = True
        except Exception as error:
            self.connected = False
            errors.append( ['Compass', 'Not connected'] )
        
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

                    if len(packlist) == 4:
    
                        self.mx = float(packlist[1])
                        self.my = float(packlist[2])
                        self.mz = float(packlist[3])
                        
                        mx_cen = self.mx-(self.mx_max + self.mx_min)/2
                        my_cen = self.my-(self.my_max + self.my_min)/2
                        
                        mx_unit = 2 * mx_cen / (self.mx_max - self.mx_min)
                        my_unit = 2 * my_cen / (self.my_max - self.my_min)
                        
                        # Magnotemeter is mounted such x is in the y direction, thus we need atan(-x,y) instead of atan(y,x)
                        angle = math.atan2( -mx_unit, my_unit)
                        # Wrap to two pi
                        self.heading = (angle) % (2 * math.pi)
                          
                        #if angle < 0:
                            #angle = angle + 2 * math.pi
                        
                        
                        
                        #self.heading = angle * (180.0/math.pi)
                        
                        #print("Heading", self.heading)
                        
                        self.data[0] = self.heading
                        self.data[1] = self.mx
                        self.data[2] = self.my
                        
                        #print(self.data[0], self.heading)
                except Exception as error:
                    print(error)
                    errors.append( ['Compass', 'Unpack failed'] )