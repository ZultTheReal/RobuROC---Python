import serial
import pynmea2

ser = serial.Serial(
    port='COM7',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0)
#setGPSmode = bytes("$PASHS,RAW,PBN,C,ON,0.5", 'utf-8')
setGPSmode = bytes("$PASHS,NME,ALL,C,OFF", 'utf-8')
#dataReq = bytes("$PASHS,RAW,MCA,C,ON,0.5", 'utf-8')

ser.write(setGPSmode)
#ser.write(dataReq)

while 1:
    num = ser.in_waiting
    if num != 0:
        line = ser.readline()
        print(line)

