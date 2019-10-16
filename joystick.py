import inputs
import math

class Joystick:
    
    gamepad = None
    killSwitch = False
    x = 0
    y = 0
    
    forward = 0.0
    rotate = 0.0

    maxJoyPos = 32768
    deadZone = 0.15 # In percent
    
    
    def __init__(self):
        self.gamepad = inputs.devices.gamepads[0]
    
    def run(self):
        
        # Get current waiting gamepad events
        events = self.gamepad.read()
    
        if( events ):
            # Loop through received gamepad events and act upon them
            for event in events:
                if(event.code == "BTN_SOUTH"):
                    self.killSwitch = ( True if event.state == 1 else False)
                elif(event.code == "ABS_X"):
                    self.x = event.state/self.maxJoyPos;
                elif(event.code == "ABS_Y"):
                    self.y = event.state/self.maxJoyPos
                #else:
                    #print(event.code )
           
            if (self.killSwitch):
                self.forward = ( self.y if abs(self.y) > self.deadZone else 0.0)
                self.rotate = (self.x if abs(self.x) > self.deadZone else 0.0)
                
            else:
                self.forward = 0.0
                self.rotate = 0.0
            
            #print( "Trans: " + "{:.2f}".format(self.transSpeed) + "m/s", "Rot: " + "{:.2f}".format(self.rotSpeed) + "m/s")
                   
    
    def getForward(self):
        return round(self.forward,4);
    
    def getRotate(self):
        return round(self.rotate,4);
            
         
