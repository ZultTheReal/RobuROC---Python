import inputs
import math

class Joystick:
    
    connected = False
    
    gamepad = None
    killSwitch = False
    x = 0
    y = 0
    
    forward = 0.0
    rotate = 0.0

    maxJoyPos = 32768
    deadZone = 0.15 # In percent
    
    
    def __init__(self):
        self.connect()
            
    def connect(self):
        if inputs.devices.gamepads:
            self.gamepad = inputs.devices.gamepads[0]
            self.connected = True
        else:
            self.gamepad = None
            
    def run(self):
        
        if self.gamepad == None:
            return False
        # Get current waiting gamepad events
        
        # collect all events
        events = []

        while(True):
            try:
                events.append(inputs.get_gamepad(blocking=False)[0])
            except inputs.UnpluggedError:
                self.forward = 0.0
                self.rotate = 0.0
                self.connected = False
                break
            except inputs.NoDataError:
                break

        if events:
            
            # If a event is received, the controller must be connected
            self.connected = True
            
            # Loop through received gamepad events and act upon them
            for event in events:
                if(event.code == "BTN_SOUTH"):
                    self.killSwitch = ( True if event.state == 1 else False)
                elif(event.code == "ABS_X"):
                    self.x = event.state/self.maxJoyPos;
                elif(event.code == "ABS_Y"):
                    self.y = event.state/self.maxJoyPos            
           
            if (self.killSwitch):
                self.forward = ( self.y if abs(self.y) > self.deadZone else 0.0)
                self.rotate = (self.x if abs(self.x) > self.deadZone else 0.0)
                
            else:
                self.forward = 0.0
                self.rotate = 0.0
            #print( "Trans: " + "{:.2f}".format(self.forward) + "m/s", "Rot: " + "{:.2f}".format(self.rotate) + "m/s")            
    
    def getForward(self):
        return round(self.forward,4);
    
    def getRotate(self):
        return round(self.rotate,4);
            
         
