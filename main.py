import time
import ApplicationSetup as apps
import Variables as var
import Functions as f
from joystick import Joystick

gamepad = Joystick()

# Variables for gampepad control
lastGamepad = 0
left = 0
right = 0


def updateTelemetry():
    apps.cur1Label['text'] = str(round( var.motCur[0], 2)) + " A"
    apps.cur2Label['text'] = str(round( var.motCur[1], 2)) + " A"
    apps.cur3Label['text'] = str(round( var.motCur[2], 2)) + " A"
    apps.cur4Label['text'] = str(round( var.motCur[3], 2)) + " A"

while(1):
    
    updateTelemetry()
    apps.app.update()
    print(var.maxSpeed)
    
    
    # Not connected to gamepad, try to reconnect
    if not gamepad.connected:
        gamepad.connect()
 
 
    if( time.time() - lastGamepad > 0.1 ):
        
        # Listen for gamepad events
        gamepad.run()
        
        lastSpeed = time.time()
        
        # Calculate left and right speeds
        left = round(gamepad.getForward() + gamepad.getRotate()/4, 2)
        right = -round(gamepad.getForward() - gamepad.getRotate()/4, 2)
        
        
        for i in range(4):
            
            if( i % 2) == 0:
                var.motorSpeed[i] = int(left * var.maxSpeed);
            else:
                var.motorSpeed[i] = int(right * var.maxSpeed);
            
            #print( "canReady: " + str( var.driveReady) )
            if( var.driveReady == True):
                
                var.network.send_message( var.addressMap[i], f.velocityArray( var.motorSpeed[i] ), remote=False )
    