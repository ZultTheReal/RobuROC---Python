import canopen
import time
import math
from .constants import *

MODE_VELOCITY = 3
MODE_CURRENT = 4



class MotorControl:
    
    setpointSpeed = [0, 0, 0, 0]
    network = None
    canReady = False
    ready = False
    periodicEnable = False
    
    errors = []
    
    # Arrays to hold actual values
    actualCur = [0, 0, 0, 0]
    actualVel = [0, 0, 0, 0]
    
    velocityDeadzone = 0.05
    
    # Arrays to hold periodic can objects 
    curPeriodic = [None, None, None, None]
    velPeriodic = [None, None, None, None]
    tempPeriodic =  [None, None, None, None]
    heartPeriodic = None
    
    controlMode = 0
    
    errors = None
    
    def __init__(self, log):
        
        self.errors = log
        self.connect()
            
    def disconnect( self ):
        
        # Make sure to kill CAN network when not using it
        if self.periodicEnable:
            for i in range(4):
                self.velPeriodic[i].stop()
                self.curPeriodic[i].stop()
                
            self.heartPeriodic.stop()
            self.periodicEnable = False
        
        if self.canReady:
            self.network.disconnect()
            self.canReady = False
        
            
    def connect( self ):
        
        if not self.isReady():
            try:
                
                self.network = canopen.Network()
                self.network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
                self.canReady = True
                
            except Exception as error:

                self.errors.append( ['CAN', 'Network not connected'] )
                self.canReady = False
        
    def setup(self):
            
        if self.canReady:

            # Stop old processes, in order to reinitiate everything
            if self.periodicEnable:
                for i in range(4):
                    self.velPeriodic[i].stop()
                    self.curPeriodic[i].stop()
                    
                self.heartPeriodic.stop()
                self.periodicEnable = False
        
            # First reset all drives
            self.resetDrive()
            time.sleep(0.5)
            
            # Setup stop deceleration limit (for smooth stop with quickStop)
            self.setDeceleration(12000000)
            
            # Enables the drives
            self.enableComm()
       
            # Enter Power Enabled
            self.switchOn()
    
            # Enter Operation Enable (ready to drive) 
            self.enableOperation()
            
            if not self.periodicEnable:
                self.startHeartbeat()
                self.startPeriodic()
                self.periodicEnable = True


            self.ready = True
        else:
            self.ready = False
            self.errors.append( ['CAN', 'Not connected to CAN bus'] )
            
            #self.dynamicBrake()
        
    def readPeriodic(self, canid, data, timestamp):

        scaled = 0   
        value = int.from_bytes(data, byteorder='little', signed=True)

        if canid in COBID_SDO_RETURN:
            # SDO data returned
            
            index = int.from_bytes(data[1:3], byteorder='little', signed=False)
            subindex = data[3]
            
            #print( index, subindex )
            
            # Temperature
            if index == 0x2021 and subindex == 0x02:

                value = int.from_bytes(data[4:8], byteorder='little', signed=True)
                print( canid, list(data), round( value/pow(2,16), 4) )
            
            #print( index, subindex )

        if canid in COBID_ACT_CURRENT:
            
            if( (canid - 897 + 1) in [2,3] ):
                value = -value
                
            scaled = round( value/SCALE_CURRENT, 4)
            index = int(COBID_ACT_CURRENT.index(canid))
            self.actualCur[index] = scaled
        
        # Returned velocity
        if canid in COBID_ACT_VELOCITY:
            
            if( (canid - 881 + 1) in [2,3] ):
                value = -value
                
            scaled = round(value/SCALE_VELOCITY*SCALE_RPM_TO_MPS, 4)
            index = int(COBID_ACT_VELOCITY.index(canid))
            self.actualVel[index] = scaled if abs(scaled) > self.velocityDeadzone else 0.0;
            
 
    def startPeriodic(self):
        #RTR - Actual Current
        for i in range(4):
            self.curPeriodic[i] = self.network.send_periodic( COBID_ACT_CURRENT[i], 8, .2, remote=True)
            self.network.subscribe( COBID_ACT_CURRENT[i], self.readPeriodic)

        #RTR - Actual Velocity
        for i in range(4):
            self.velPeriodic[i] = self.network.send_periodic( COBID_ACT_VELOCITY[i], 8, .025, remote=True)
            self.network.subscribe( COBID_ACT_VELOCITY[i], self.readPeriodic)
           
        # SDO - Temperature 
        #for i in range(4):
            #packet = self.sdoPacket( 0x2021, 0x01 )
            #self.tempPeriodic[i] = self.network.send_periodic( COBID_SDO[i], packet, .1, remote=False)
            #self.network.subscribe( COBID_SDO_RETURN[i], self.readPeriodic)
 
 
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
        
        self.heartPeriodic = self.network.send_periodic( 0x700 + COBID_HOST, [0], 0.1, remote=False)
    
    # print('[{}]'.format(', '.join(hex(x) for x in data)))
 
    def isReady(self):
        return self.canReady
    
    
    def sendCanPacket(self, cobId, data ):
        try:
            self.network.send_message( cobId, data )
        except Exception as error:

            self.errors.append( ['CAN', "{:02x}".format(cobId) +':'+ str(data) + ' - ' + error.args[0]] )
            
 
    def setSpeed(self, index = 0, speed = 0):
        if self.ready:
            if isinstance(speed, int):
                # Convert speed to bytearray for sending over CAN
                #print( "Speed: " , speed )
                #if speed == 0:
                    # Change mode
                    #self.setMode(MODE_CURRENT)
                    
                    # Set current to zero, dont use velocity
                    #current = 0
                    
                    #data = (current).to_bytes(4, byteorder="little", signed=True)
                    #self.sendCanPacket( COBID_TAR_CURRENT[index], [0] )
                #else:
                    
                    # Change mode
                self.setMode(MODE_VELOCITY)
                    
                data = (speed).to_bytes(4, byteorder="little", signed=True)
                self.sendCanPacket( COBID_TAR_VELOCITY[index], list(data) )
                
            else:
                raise TypeError('Unvalid speed type')
    
    def setCurrent(self, index = 0, current = 0):
        
        if self.ready:
            value = int(current * SCALE_SETCURRENT)
            
            self.setMode(MODE_CURRENT)
            
            data = (value).to_bytes(4, byteorder="little", signed=True)
            self.sendCanPacket( COBID_TAR_CURRENT[index], list(data) )
                
    
    def setMode( self, mode ):
        
        # Control word ( enable operation )
        prepend = [0x0F, 0]
        
        # Only change mode if the current mode is different
        if self.controlMode != mode:
            data = (mode).to_bytes(1, byteorder="little", signed=True)
            
            for i in range(4):
                self.sendCanPacket( COBID_MODE[i], prepend + list(data) ) 
            
            self.controlMode = mode
            
    # Set speed in Rad/s
    def setRPS( self, index = 0, rad = 0):
        
        speed = ( rad * 60.0/(2*math.pi) ) * SCALE_VELOCITY
        
        self.setSpeed( index, int(speed) )
        
    
    def setMPS( self, index = 0, mps = 0 ):
        
        
        # Convert speed (m/s) to motor speed value
        speed = mps * (SCALE_VELOCITY/SCALE_RPM_TO_MPS)
        #print(speed)
        self.setSpeed( index, int(speed) )
    
    
    def setRPM( self, index = 0, rpm = 0 ):
        
        
        # Convert speed (m/s) to motor speed value
        speed = rpm * SCALE_VELOCITY
        #print(speed)
        self.setSpeed( index, int(speed) )


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
      
    def dynamicBrake(self):
        
        data = [0x80F, 0]
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
        
        data = self.sdoPacket(index, subindex)
            
        self.sendCanPacket(COBID, data)
        
        # Now read packet from PCAN-VIEW <3
        
    def sdoPacket(self, index = 0, subindex = 0 ):
        
        commandByte = [0x40]
        
        # Convert object index into two bytes and append the subindex
        indexBytes = list( (index).to_bytes(2, byteorder="little", signed=False) )
        indexBytes.append(subindex)
        
        data = commandByte + indexBytes
        
        # Append zeroes if data is less than 8 bytes long
        for i in range(8-len(data)):
            data.append(0)
        
        return data
    
    def setDeceleration(self, value):
        
        valueBytes = (value).to_bytes(4, byteorder="little", signed=True)
        data = list(valueBytes)
    
        for i in range(4):
            self.sdoWrite( COBID_SDO[i], data, INDEX_DECELERATION_LIMIT, SUBINDEX_DECELERATION_LIMIT )
            
            
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