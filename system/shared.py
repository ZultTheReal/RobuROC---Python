from .motorControl import MotorControl
from .dataLogger import Logging


# Motor controller object as this is used between the other objects aswell
motors = MotorControl()



# Logging object
log = Logging('measurements')

class SharedVariables:

    # Variables for gui to act with main
    gamepadEnabled = False
    
    loggingEnabled = False
    
    gpsConnected = False
    imuConnected = False
    

var = SharedVariables()