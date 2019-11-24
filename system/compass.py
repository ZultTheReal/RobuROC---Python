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
    
    def __init__(self):
        self.heading = 0     # Heading measurement from OS5000 (not accurate, because it is mounted on a fawking stick.
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
                timeout=0.05
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
                        
                        # https://arduino.stackexchange.com/questions/18625/converting-three-axis-magnetometer-to-degrees
                        angle = 90 - math.atan2(my_unit, -mx_unit)
                        
                        if angle < 0:
                            angle = angle + 2 * math.pi
                            
                        self.heading = angle * 180.0/math.pi
                        
                        self.data[0] = self.heading
                        self.data[1] = self.mx
                        self.data[2] = self.my
                        
                        #print(self.data[0], self.heading)
                except Exception as error:
                    print(error)
                    errors.append( ['Compass', 'Unpack failed'] )