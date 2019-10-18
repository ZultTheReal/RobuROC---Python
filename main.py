import time
import ApplicationSetup as apps
import Variables as var
import Functions as f
from joystick import Joystick

gamepad = Joystick()

motorSpeed = {
    0: 0,
    1: 0,
    2: 0,
    3: 0
}

# Variables for gampepad control
lastGamepad = 0
left = 0
right = 0

maxSpeed = 3000000;

def updateTelemetry():
    apps.cur1Label['text'] = str(round( var.motCur[0], 2)) + " A"
    apps.cur2Label['text'] = str(round( var.motCur[1], 2)) + " A"
    apps.cur3Label['text'] = str(round( var.motCur[2], 2)) + " A"
    apps.cur4Label['text'] = str(round( var.motCur[3], 2)) + " A"

while(1):
    
    updateTelemetry()
    apps.app.update()
    
    
    # Not connected to gamepad, try to reconnect
    if not gamepad.connected:
        gamepad.connect()
 
 
    if( time.time() - lastGamepad > 0.1 ):
        
        # Listen for gamepad events
        gamepad.run()
        
        lastSpeed = time.time()
        
        # Calculate left and right speeds
        left = round(gamepad.getForward() + gamepad.getRotate(), 2)
        right = -round(gamepad.getForward() - gamepad.getRotate(), 2)
        
        
        for i in range(4):
            
            if( i % 2) == 0:
                motorSpeed[i] = int(left * maxSpeed);
            else:
                motorSpeed[i] = int(right * maxSpeed);
            
            print( "canReady: " + str( var.driveReady) )
            if( var.driveReady == True):
                
                var.network.send_message( var.addressMap[i], f.velocityArray( motorSpeed[i] ), remote=False )
    