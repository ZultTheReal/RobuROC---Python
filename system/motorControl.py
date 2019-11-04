import canopen
import time
from .constants import *

class MotorControl:
    
    setpointSpeed = [0, 0, 0, 0]
    network = None
    canReady = False
    
    errors = []
    
    # Arrays to hold actual values
    actualCur = [0, 0, 0, 0]
    actualVel = [0, 0, 0, 0]
    
    # Arrays to hold periodic can objects 
    curPeriodic = [None, None, None, None]
    velPeriodic = [None, None, None, None]
    
    def __init__(self):
        
        self.connect()
            
    def disconnect( self ):
        
        # Make sure to kill CAN network when not using it

        self.network.disconnect()
        self.canReady = False
        
            
    def connect( self ):
        
        if not self.isReady():
            try:            
                self.network = canopen.Network()
                self.network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
                self.canReady = True
                
            except Exception as error:
                self.canReady = False
        
    def setup(self):
        
        if self.canReady:
            # First reset all drives
            self.resetDrive()
            
            time.sleep(0.5)
            
            self.startHeartbeat()
            self.startPeriodic()
            
            # Setup stop deceleration limit (for smooth stop with quickStop)
            self.setDeceleration(12000000)
            
            # Enables the drives
            self.enableComm()
            
            # Enter Power Enabled
            self.switchOn()
            
            # Enter Operation Enable (ready to drive) 
            self.enableOperation() 
        
    def readPeriodic(self, canid, data, timestamp):

        scaled = 0
        value = int.from_bytes(data, byteorder='little', signed=True)


        if canid in COBID_ACT_CURRENT:
            scaled = round( value/SCALE_CURRENT, 2)
            index = int(COBID_ACT_CURRENT.index(canid))
            self.actualCur[index] = scaled

        if canid in COBID_ACT_VELOCITY:
            scaled = round(value/SCALE_VELOCITY*SCALE_RPM_TO_MPS, 2)
            index = int(COBID_ACT_VELOCITY.index(canid))
            self.actualVel[index] = scaled
            
 
    def startPeriodic(self):
        #RTR - Actual Current
        for i in range(4):
            self.curPeriodic[i] = self.network.send_periodic( COBID_ACT_CURRENT[i], 8, .1, remote=True)
            self.network.subscribe( COBID_ACT_CURRENT[i], self.readPeriodic)

        #RTR - Actual Velocity
        for i in range(0, 4):
            self.velPeriodic[i] = self.network.send_periodic( COBID_ACT_VELOCITY[i], 8, .1, remote=True)
            self.network.subscribe( COBID_ACT_VELOCITY[i], self.readPeriodic)
            
 
    def isReady(self):
        return self.canReady
    
    
    def sendCanPacket(self, cobId, data ):
        try:
            self.network.send_message( cobId, data )
        except Exception as error:
            self.errors.append(error)
            
 
    def setSpeed(self, index = 0, speed = 0):

        if isinstance(speed, int):
            # Convert speed to bytearray for sending over CAN
            data = (speed).to_bytes(4, byteorder="little", signed=True)
            
            self.sendCanPacket( COBID_TAR_VELOCITY[index], list(data) )
        else:
            raise TypeError('Unvalid speed type')
    
    def setRPM( self, index = 0, rpm = 0 ):
        
        # Convert speed (m/s) to motor speed value
        speed = rpm / SCALE_VELOCITY
        self.setSpeed( index, speed )
    
    # --- Communication state machine functions ---
    
    def enableComm(self):
        # Enable all drives with global NMT command
        # Reset command: 0x01
        self.sendCanPacket(0, [0x1, 0])
    
    def stopComm(self):
        # Transitions the drives into quick stop state with a NMT message
        # Stop command: 0x02
        self.sendCanPacket(0, [0x02, 0])
    
    def resetDrive(self):
        # Reset all drives with one global NMT command
        # Reset command: 0x81
        self.sendCanPacket(0, [0x81, 0])


    # --- Operational state machine functions ---
    
    def disableVoltage(self):
        # Disable all drives with PDO message
        # To disable the voltage the drive must be in quick stop state
        # Disable Voltage command: 0x00
        data = [0x0, 0]
        for i in range(4):
            self.sendCanPacket(COBID_CONTROL[i], data)

    def quickStop(self):
        # Transitions the drives into quick stop state with a PDO message
        # Quick Stop command: 0x02
        data = [0x02, 0]
        for i in range(4):
            self.sendCanPacket(COBID_CONTROL[i], data)

    def shutDown(self):
        # Shutdown the drives with a PDO message
        # Shutdown command: 0x06
        data = [0x06, 0]
        for i in range(4):
            self.sendCanPacket(COBID_CONTROL[i], data)
            
    def enableOperation(self):
        # Enable operation
        data = [0x0F, 0]
        for i in range(4):
            self.sendCanPacket(COBID_CONTROL[i], data)
            
    def switchOn(self):
        # Turn on the drives with PDO message
        # Switch on command: 0x07
        data = [0x07, 0]
        for i in range(4):
            self.sendCanPacket(COBID_CONTROL[i], data)
      
      
    def sdoWrite(self, COBID = 0, data = None, index = 0, subindex = 0 ):
    
        if( len( data ) <= 4 ):
            
            # Command byte for writing 4 bytes SDO
            # 0x22 describes this that is is a 4 byte SDO message from host 
            commandByte = [0x22]
            
            # Convert object index into two bytes and append the subindex
            indexBytes = list( (index).to_bytes(2, byteorder="little", signed=False) )
            indexBytes.append(subindex)
            
            data = commandByte + indexBytes + data
            
            # Append zeroes if data is less than 8 bytes long
            for i in range(8-len(data)):
                data.append(0)
            
            # Now send message over CAN-network
            # print('[{}]'.format(', '.join(hex(x) for x in data)))
            
            self.sendCanPacket(COBID, data)
            
        else:
            raise NotImplementedError( "Data lenght is not supported")


    def sdoRead(self, COBID = 0, index = 0, subindex = 0 ):
        
        commandByte = [0x40]
        
        # Convert object index into two bytes and append the subindex
        indexBytes = list( (index).to_bytes(2, byteorder="little", signed=False) )
        indexBytes.append(subindex)
        
        data = commandByte + indexBytes
        
        # Append zeroes if data is less than 8 bytes long
        for i in range(8-len(data)):
            data.append(0)
            
        self.sendCanPacket(COBID, data)
        
        # Now read packet from PCAN-VIEW <3
    
    def setDeceleration(self, value):
        
        valueBytes = (value).to_bytes(4, byteorder="little", signed=True)
        data = list(valueBytes)
    
        for i in range(4):
            self.sdoWrite( COBID_SDO[i], data, INDEX_DECELERATION_LIMIT, SUBINDEX_DECELERATION_LIMIT )
            

    def startHeartbeat(self):
    
        # Consumer Heartbeat object address is 0x1016, with sub-index 01 (page 75 comm manual)
        
        # Consumertime Limited between 1-65535 (16-bit unsigned int)
        consumerTime = 200 # ms
        timeInBytes = (consumerTime).to_bytes(2, byteorder="little", signed=False)
        
        
        data = list(timeInBytes)
        data.append(COBID_HOST) # Configure all motor driver nodes to listen for heartbeat from HOST
    
        for i in range(4):
            self.sdoWrite( COBID_SDO[i], data, INDEX_HEARTBEAT, SUBINDEX_HEARTBEAT )
            
        time.sleep(0.1)
        
        # Begin heartbeat
        
        self.network.send_periodic( 0x700 + COBID_HOST, [0], 0.1, remote=False)
    
    # print('[{}]'.format(', '.join(hex(x) for x in data)))

    def pause(self):
        self.quickStop()
        
    def start(self):
        self.enableOperation()
        
        
# Read Ki
#mc.sdoRead( const.COBID_SDO[0], 0x2032, 0x08 )

# Read Ks
#mc.sdoRead( const.COBID_SDO[0], 0x20D8, 0x24 )

# Read Resolver resolution
#mc.sdoRead( const.COBID_SDO[0], 0x2032, 0x06 )