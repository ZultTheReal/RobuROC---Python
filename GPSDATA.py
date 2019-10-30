import serial
import operator
from functools import reduce

class GPSclass:
    ser = None

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
            timeout=0)
            print("GPS connected to: " + self.ser.portstr)
            setupGPS(self.ser)
            return 0
        except Exception as e:
            print(e)
            print("ERROR: GPS not connected, tried to connect to: " + comPort)
            return -1

    def getData(self):
        try:
            bytesWaiting = self.ser.in_waiting
        except:
            print('Error: Can\'t read data, no connection to the GPS')
            return -1 

        if bytesWaiting != 0:
            nmea_string = str(self.ser.readline(),'UTF-8')
            newData = translateGPSData(self,nmea_string)
            if (newData == 1):
                return 0 #New data succesfully added return 0
        return -1 #Something went wrong, no new data, return -1



def checksum(nmea_str):
    return reduce(operator.xor, map(ord, nmea_str), 0)

def translateGPSData(GPSc,nmea_str):
    nmea_str = nmea_str.replace('$','') # Remove dollar sign (not needed/not to be counted in CRC)
    temp = nmea_str.split("*") #Remove checksum at end of nmea_str and save 
    try:
        CRC1 = int(temp[1], 16) #convert checksum to integer from hex nmea_str
    except:
        #print('Error: No checksum')
        # GPSc.clear() clear data?????
        return -1
    nmea_str = temp[0] 
    CRC2 = checksum(nmea_str) #Calculate checksum for received nmea_str 

    if (CRC1 == CRC2): # if the two checksums match update the GPS info
        temp = nmea_str.split(",")
        GPSc.sat_count = int('0'+temp[3])
        GPSc.timestamp = float('0'+temp[4])
        GPSc.latitude = float('0'+temp[5]) #In format ddmm.mmmmmm
        GPSc.latitude = round(int(GPSc.latitude / 100) + (GPSc.latitude - int(GPSc.latitude/100.0)*100.0)/60.0,6) #latitude degree
        GPSc.latitude_dir = temp[+6]
        GPSc.longitude = float('0'+temp[7]) #In format dddmm.mmmmmm
        GPSc.longitude = round(int(GPSc.longitude / 100) + (GPSc.longitude - int(GPSc.longitude/100.0)*100.0)/60.0,6) #longtitude degree
        GPSc.longitude_dir = temp[8]
        GPSc.altitude = float('0'+temp[9])
        GPSc.heading = float('0'+temp[11])
        GPSc.linear_speed = float('0'+temp[12])
        GPSc.rate_of_climb = float('0'+temp[13])
        return 0
    else:
        #print('Error: Checksums doesn\'t match')
        # GPSc.clear() clear data?????
        return -1  

def setupGPS(ser):
    ser.write("$PASHS,POP,20")
    ack =  str(self.ser.readline(),'UTF-8')
    print("Respone to $PASHS,POP,20: " + ack)
    if ack != "$PASHR,ACK*3D":
        return -1
    ser.write("$PASHS,NME,POS,B,ON,0.05")
    ack =  str(self.ser.readline(),'UTF-8')
    print("Respone to $PASHS,NME,POS,B,ON,0.05: " + ack)
    #if ack != "$PASHR,ACK*3D"
    #   return -1
    return 0

# Test code 
#GPS = GPSclass()
#GPS.connect('COM6')
#GPS.getData()


# For testing the translator
# GPS = GPSclass()
# temp = '$PASHR,POS,0,6,123422.00,5700.8796880,N,00959.1834680,E,053.063,,000.0,000.000,+000.000,3.6,2.3,2.7,2.4,Hp23*12'
#translateGPSData(GPS,temp)
#print(GPS)
