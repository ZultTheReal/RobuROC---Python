import canopen
import time
import constants as const

class MotorDrives:
    
    setpointSpeed = [0, 0, 0, 0]
    network = None
    
    # Arrays to hold actual values
    actualCur = [0, 0, 0, 0]
    actualVel = [0, 0, 0, 0]
    
    # Arrays to hold periodic can objects 
    curPeriodic = [None, None, None, None]
    velPeriodic = [None, None, None, None]
    
    def __init__(self, network):
        self.network = network

        
    def ignition(self):
        
        # First reset all drives
        self.resetDrive()
        
        self.configureHeartbeat()
        self.configurePeriodic()
        
        # Enables the drives
        self.enableDrive()
        
        # Enter Power Enabled
        self.switchOn()
        
        # Enter Operation Enable (ready to drive) 
        self.enableOperation() 
        
    def readPeriodic(self, canid, data, timestamp):

        scaled = 0
        value = int.from_bytes(data, byteorder='little', signed=True)

        if canid in const.COBID_ACT_CURRENT:
            scaled = value/const.SCALE_CURRENT
            index = int(const.COBID_ACT_CURRENT.index(canid))
            self.actualCur[index] = scaled

        if canid in const.COBID_ACT_VELOCITY:
            scaled = value/const.SCALE_VELOCITY * 0.108
            index = int(const.COBID_ACT_VELOCITY.index(canid))
            self.actualVel[index] = scaled
            
 
    def configurePeriodic(self):
        #RTR - Actual Current
        for i in range(4):
            self.curPeriodic[i] = self.network.send_periodic( const.COBID_ACT_CURRENT[i], 8, .1, remote=True)
            self.network.subscribe( const.COBID_ACT_CURRENT[i], self.readPeriodic)

        #RTR - Actual Velocity
        for i in range(0, 4):
            self.velPeriodic[i] = self.network.send_periodic( const.COBID_ACT_VELOCITY[i], 8, .1, remote=True)
            self.network.subscribe( const.COBID_ACT_VELOCITY[i], self.readPeriodic)
            
 
    def setSpeed(self, motorIndex = 0, speed = 0):
        if isinstance(speed, int):
            
            # Convert speed (m/s) to motor speed value

            # Convert speed to bytearray for sending over CAN
            data = (speed).to_bytes(4, byteorder="little", signed=True)
            
            self.network.send_message( const.COBID_TAR_VELOCITY[i], list(data) )
            
            #  print( prepend + list(data) )
    
    
    # --- Communication state machine functions ---
    
    def enableDrive(self):
        # Enable all drives with global NMT command
        # Reset command: 0x01
        for i in range(4):
            network.send_message(0, [0x1, i])
    
    def stopDrive(self):
        # Transitions the drives into quick stop state with a NMT message
        # Stop command: 0x02
        for i in range(4):
            network.send_message(0, [0x02, i])
    
    def resetDrive(self):
        # Reset all drives with global NMT command
        # Reset command: 0x81
        for i in range(4):
            network.send_message(0, [0x81, i])
            time.sleep(.2) # Sleep a little to not stress the network??? 

    
    # --- Operational state machine functions ---
    
    def disableVoltage(self):
        # Disable all drives with PDO message
        # To disable the voltage the drive must be in quick stop state
        # Disable Voltage command: 0x00
        data = [0x0, 0]
        for i in range(4):
            network.send_message(0x201, data)

    def quickStop(self):
        # Transitions the drives into quick stop state with a PDO message
        # Quick Stop command: 0x02
        data = [0x02, 0]
        for i in range(4):
            network.send_message(const.COBID_CONTROL[i], quickStop)

    def shutDown(self):
        # Shutdown the drives with a PDO message
        # Shutdown command: 0x06
        data = [0x06, 0]
        for i in range(4):
            network.send_message(const.COBID_CONTROL[i], data)
            
    def enableOperation(self):
        # Enable operation
        data = [0x0F, 0]
        for i in range(4):
            network.send_message(const.COBID_CONTROL[i], data)
            
    def switchOn(self):
        # Turn on the drives with PDO message
        # Switch on command: 0x07
        data = [0x07, 0]
        for i in range(4):
            network.send_message(const.COBID_CONTROL[i], data)
      
      
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
            
            self.network.send_message(COBID, data)


    def sdoRead(self, COBID = 0, index = 0, subindex = 0 ):
        
        commandByte = [0x40]
        
        # Convert object index into two bytes and append the subindex
        indexBytes = list( (index).to_bytes(2, byteorder="little", signed=False) )
        indexBytes.append(subindex)
        
        data = commandByte + indexBytes
        
        # Append zeroes if data is less than 8 bytes long
        for i in range(8-len(data)):
            data.append(0)
            
        self.network.send_message(COBID, data)


    def configureHeartbeat(self):
    
        # Consumer Heartbeat object address is 0x1016, with sub-index 01 (page 75 comm manual)
        
        # Consumertime Limited between 1-65535 (16-bit unsigned int)
        consumerTime = 200 # ms
        timeInBytes = (consumerTime).to_bytes(2, byteorder="little", signed=False)
        
        
        data = list(timeInBytes)
        data.append(const.COBID_HOST) # Configure all motor driver nodes to listen for heartbeat from HOST
    
        for i in range(4):
            self.sdoWrite( const.COBID_SDO[i], data, const.INDEX_HEARTBEAT, const.SUBINDEX_HEARTBEAT )
            
        time.sleep(0.1)
        
        # Begin heartbeat
        
        self.network.send_periodic(0x705, [0], 0.1, remote=False)
    
    # print('[{}]'.format(', '.join(hex(x) for x in data)))

        
            
network = canopen.Network()
network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)
        
mc = MotorDrives(network);

mc.ignition()

time.sleep(0.1)

mc.sdoRead( 0x602, 0x2032, 0x08 )

time.sleep(1)

#for i in range(4):
    #mc.setSpeed( i, 1000000 )

#while( 1 ):
    #print(mc.actualVel)