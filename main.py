
# Import the classes for interfacing with the RobuROC
import system as car

import random


# Application object
gui = car.Interface()

# Logging object
log = car.Logging('measurements')



class Shit:
    
    other = [0, 0, 0]
    data = [0, 0]
    
    def doDis(self):
        self.data[0] = random.randint(1,5)
        self.data[1] = random.randint(1,10)
        
        self.other[0] = random.randint(1,200)
        self.other[1] = random.randint(1,100)
        self.other[2] = random.randint(1,400)

shit = Shit()



number1 = 0



log.addMeasurements( shit.data, ['X1','X2'])
log.addMeasurements( shit.other, [ 'X3','X4','X5'] )

log.begin()


#motors = MotorControl()
#motors.setup()


# Read Ki
#mc.sdoRead( const.COBID_SDO[0], 0x2032, 0x08 )

# Read Ks
#mc.sdoRead( const.COBID_SDO[0], 0x20D8, 0x24 )

# Read Resolver resolution
#mc.sdoRead( const.COBID_SDO[0], 0x2032, 0x06 )

#for i in range(4):
    #motors.setSpeed(i, 2000000)

while( 1 ):
    
    shit.doDis()
    
    log.update(0.1, 100)
    
    pass
    #app.update()
    #print(motors.actualVel)