import serial
import operator
from functools import reduce
import time
import utm
import math
from .shared import *

class GPS:

    ser = serial.Serial()
    data = [0, 0, 0, 0, 0] #Heading, latitude, lontitude, linear_speed
    connected = False
    
    dataReady = 0;
    
    utmData = [0, 0]

    def __init__(self):
        self.clear()

    def clear(self):
        self.sat_count = 0          # Number of connected satellites
        self.timestamp = 0          # timestamp
        self.latitude = 0           # lateral coordinate
        self.latitude_dir = 0       # lateral direction (North,South)
        self.longitude = 0          # Longitudinal coordinate
        self.longitude_dir = 0      # Longitudinal direction (West,East)
        self.altitude = 0           # Altitude
        self.heading = 0            # Which direction the vehicle is heading
        self.linear_speed = 0
        self.rate_of_climb = 0      # Vertical speed (uphill)
        self.filter_speed = 0
        self.available = 0
    def __str__(self):
       return f'Satellite Count: {self.sat_count}   Timestamp: {self.timestamp}  Latitude: {self.latitude}   Latitude Direction: {self.latitude_dir}   Longitude: {self.longitude}   Longitude Direction: {self.longitude_dir}   Heading: {self.heading}   Linear_speed: {self.linear_speed}'

    def connect(self,comPort):
        try:
            self.ser = serial.Serial(
                port= comPort,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.03
            )
            
            self.setup()
            self.connected = True

        except Exception as error:
            
            self.connected = False
            errors.append( ['GPS', 'Not connected'] )

    def setup(self):
        self.ser.write("$PASHS,POP,20\r\n".encode('UTF-8')) #Return to standard settings
        time.sleep(0.2)
        #ack =  self.ser.readline().decode().strip('\r\n')
        #print(ack)
        #if ack != "$PASHR,ACK*3D":
        #    return -1

        self.ser.write("$PASHS,NME,POS,B,ON,0.05\r\n".encode('UTF-8')) #output messages with 20 Hz
        time.sleep(0.2)
        #ack =  self.ser.readline().decode().strip('\r\n')
        #print(ack)
        #if ack != "$PASHR,ACK*3D"
        #   return -1
        return 0
    
    def getNewestData(self):

        data = self.getUTM();
        speed = self.linear_speed;
        status = self.dataReady;
        
        if self.dataReady:
            self.dataReady = 0
  
        return data, speed, status

    def readData(self):
        
        try:
            bytesWaiting = self.ser.in_waiting
            self.connected = True
        except Exception as error:
            self.connected = False
        
        if self.connected:
            
            try:
                tempString = ''
                while self.ser.in_waiting !=0:
                    tempString = self.ser.readline().decode().strip('\r\n')
            except Exception as error:
                self.connected = False
                print("ERROR", error)
        
            # Every line from buffer is read, now use the newest to get data
            if tempString != '':

                # Unpack nmea string and save data in class
                self.dataReady = self.unpack(tempString)
                

    def checksum(self,nmea_str):
        return reduce(operator.xor, map(ord, nmea_str), 0)
    
    def getUTM(self):
        
        east, north, number, zone = utm.from_latlon( self.latitude, self.longitude )
        
        return [east, north]
    
    
    def unpack(self,nmea_str):
        
        nmea_str = nmea_str.replace('$','') # Remove dollar sign (not needed/not to be counted in CRC)
        temp = nmea_str.split("*") #Remove checksum at end of nmea_str and save
        
        if len(temp) is 2 and temp[1] is not '':
            
            try:
                CRC1 = int(temp[1], 16) #convert checksum to integer from hex nmea_str

                nmea_str = temp[0] 
                CRC2 = self.checksum(nmea_str) #Calculate checksum for received nmea_str
            except Exception as error:
                errors.append( ['GPS', 'Weird checksum error'] )
                return 0
            
            if CRC1 is CRC2: # if the two checksums match update the GPS info
                temp = nmea_str.split(",")
                
                try:
                    self.sat_count = int(temp[3])
                    self.timestamp = self.floatOrZero(temp[4])
                    self.latitude = self.floatOrZero(temp[5]) #In format ddmm.mmmmmm
                    self.latitude = round(int(self.latitude / 100) + (self.latitude - int(self.latitude/100.0)*100.0)/60.0,15) #latitude degree
                    self.latitude_dir = temp[6]  
                    self.longitude = self.floatOrZero(temp[7]) #In format dddmm.mmmmmm
                    self.longitude = round(int(self.longitude / 100) + (self.longitude - int(self.longitude/100.0)*100.0)/60.0,15) #longtitude degree
                    self.longitude_dir = temp[8]
                    self.altitude = self.floatOrZero(temp[9])
                    
                    # Convert to radians
                    angle = 2*math.pi - self.floatOrZero(temp[11]) * math.pi/180;
                    angle = angle + math.pi/2;
                    # Wrap to pi
                    self.heading = (angle) % (2 * math.pi)
                    
                    self.linear_speed = round(self.floatOrZero(temp[12]) * 0.5144, 5)
                    self.rate_of_climb = self.floatOrZero(temp[13])
                    
                    # self.filter_speed = self.LPF(self.linear_speed, self.filter_speed, 0.1)
                    
                    utmdat = self.getUTM()
                    self.utmData[0] = utmdat[0]
                    self.utmData[1] = utmdat[1]
                        
                        
                    if (self.linear_speed and self.heading) is 0.0:
                        
                        for i in range(5):
                            self.data[i] = 0.0
                        
                        return 0
            
                except Exception as error:
                    print(error)
                    errors.append( ['GPS', 'Could not unpack data'] )
                    return 0
                
                #Heading, latitude, lontitude, linear_speed
                self.data[0] = self.heading
                self.data[1] = self.latitude
                self.data[2] = self.longitude
                self.data[3] = self.linear_speed
                self.data[4] = self.sat_count
                
                if self.sat_count != 0:
                    return 1
                
                return 0
    
            else:
                errors.append( ['GPS', 'Checksum doesn\'t match'] )
                #print(temp)
                
            return 0
    
    def LPF( self, newSample, oldSample, alpha ):
        return (alpha * newSample) + (1.0-alpha) * oldSample  

    
    def floatOrZero(self,strValue):
        if (strValue != ""):
            return float(strValue)
        else:
            return 0.0



# Test code 
# GPS = GPSclass()
# GPS.connect('COM10')

# for i in range(0,10):
#     GPS.getData()
#     print(GPS)
#     time.sleep(0.1)



# For testing the translator
# GPS = GPSclass()
# temp = '$PASHR,POS,0,6,123422.00,5700.8796880,N,00959.1834680,E,053.063,,000.0,000.000,+000.000,3.6,2.3,2.7,2.4,Hp23*12'
# GPS.translateGPSData(temp)
# print(GPS)
