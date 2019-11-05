from .motorControl import MotorControl
from .logging import Logging

errors = []

# Motor controller object as this is used between the other objects aswell
motors = MotorControl()

class Variables:

    # Variables for gui to act with main
    gamepadEnabled = False
    
    loggingEnabled = False
    
    gpsConnected = False
    imuConnected = False
    

var = Variables()

# Logging object
log = Logging('measurements')