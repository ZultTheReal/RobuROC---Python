import serial
import time
import math 

class Compass:
    
    connected = False
    data = [0] # Heading 
    
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
                        
                        
    
                        self.heading = float(packlist[0])
                        self.mx = float(packlist[1])
                        self.my = float(packlist[2])
                        self.mz = float(packlist[3])
                        
                        self.data[0] = math.atan2(self.my, -self.mx) * 180.0/math.pi

                except Exception as error:
                    print(error)
                    errors.append( ['Compass', 'Unpack failed'] )