#  Copyright Emil Jacobsen (SolidGeek)
#
#  This is a heavily simplified/modified version of joncoop's pygame-xbox360controller
#
#      <https://github.com/joncoop/pygame-xbox360controller>.

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
from .shared import *

class InputMap:
    # Digital inputs (buttons)
    A = 0 # Button A
    B = 1 # Button B
    X = 2 # Button X
    Y = 3 # Button Y
    LB = 4 # Button LB
    RB = 5 # Button RB
    BACK = 6 # Button BACK
    START = 7 # Button START
    LS = 8 # Left stick button
    RS = 9 # Right stick button
    
    # Analog inputs (axis)
    LX = 0 # Left stick x
    LY = 1 # Left stick y
    LT = 2 # Left trigger 
    RX = 4 # Rigth stick x
    RY = 3 # Rigth stick y
    RT = 2 # Right trigger
    
    xAxis = 0
    yAxis = 1

class Gamepad:
    
    joystick = None
    joystick_id = 0
    connectStatus = True
    
    refresh_time = 0 
    refresh_delay = 0
    
    comm_alive = 0 # Last time an button or x-axis was moved
    
    reconnect_delay = 1.0 # Delay between trying to reconnect
    reconnect_time = 0

    def __init__(self, dead_zone = 0.15, refresh_rate = 100, id = 0):
        """
        Initializes the joystick (xbox) connected.

        Args:
            dead_zone: The size of dead zone for the analog sticks (default 0.15)
            refreshRate: The frequency of which the joystick is read
        """
        
        self.joystick_id = id
        self.refresh_time = 0
        self.refresh_delay = 1/refresh_rate # Calculate the refreshdelay in seconds
        self.dead_zone = dead_zone
    
        
        # Init the pygame engine, which supports xbox controller inputs
        pygame.init()
        pygame.joystick.init()
        
        self.connect()
        
        
        
        # As soon as refresh() is called, the class tries to connect to a gamepad

    def refresh(self):
        
        self.connect()
        
        if self.refresh_time < time.time():
            
            # Define next refresh time
            self.refresh_time = time.time() + self.refresh_delay                

            # Read pygame events (needed to read joystick), return the events for debugging purposes
            for event in pygame.event.get():
                self.comm_alive = time.time()
         

    def connect(self):

        # Only try to reconnect, if there has elapsed the appropiated time since last attempt
        if time.time() - self.reconnect_time > self.reconnect_delay:
            
            
            self.reconnect_time = time.time()
            
            # Reinitiaze the joystick instance in the pygame object to get current joystick count - takes zero time
            pygame.joystick.quit()
            pygame.joystick.init()

            # Count number of connections
            count = pygame.joystick.get_count()
            
            if( count >= 1 ):
                self.joystick = pygame.joystick.Joystick(self.joystick_id)
                self.joystick.init()
                
                if not self.connectStatus:
                    self.connectStatus = True
                    errors.append( ['Joystick', 'Connected'] )
            else:
                
                errors.append( ['Joystick', 'Connecting...'] )
                
                if self.connectStatus:
                    self.connectStatus = False
                    errors.append( ['Joystick', 'Not connected'] )
                

    def connected(self):
        
        return self.connectStatus
    

    def dead_zone_adjustment(self, value):
        """
        Analog sticks likely wont ever return to exact center when released. Without
        a dead zone, it is likely that a small axis value will cause game objects
        to drift. This adjusment allows for a full range of input while still
        allowing a little bit of 'play' in the dead zone.

        Returns:
            Axis value outside of the dead zone remapped proportionally onto the
            -1.0 <= value <= 1.0 range.
        """

        if value > self.dead_zone:
            return (value - self.dead_zone) / (1 - self.dead_zone)
        elif value < -self.dead_zone:
            return (value + self.dead_zone) / (1 - self.dead_zone)
        else:
            return 0

    def buttons(self):
        """
        Gets the state of each button on the controller.

        Returns:
            A tuple with the state of each button. 1 is pressed, 0 is unpressed.
        """
        
        buttons = [0 for row in range(10)]
        
        self.refresh()
        
        if( self.connectStatus ):
        
            buttons = [
                self.joystick.get_button( InputMap.A ), 
                self.joystick.get_button( InputMap.B ),
                self.joystick.get_button( InputMap.X ),
                self.joystick.get_button( InputMap.Y ),
                self.joystick.get_button( InputMap.LB ),
                self.joystick.get_button( InputMap.RB ),
                self.joystick.get_button( InputMap.LS ),
                self.joystick.get_button( InputMap.RS ),
                self.joystick.get_button( InputMap.BACK ),
                self.joystick.get_button( InputMap.START ),
            ]
            
        return buttons;


    def left_stick(self):
        """
        Gets the state of the left analog stick.

        Returns:
            The x & y axes as a tuple such that

            -1 <= x <= 1 && -1 <= y <= 1

            Negative values are left and down.
            Positive values are right and up.
        """
        lx = 0
        ly = 0
        
        self.refresh()
        
        if( self.connectStatus ):  
            lx = self.dead_zone_adjustment( self.joystick.get_axis( InputMap.LX ) )
            ly = self.dead_zone_adjustment( -self.joystick.get_axis( InputMap.LY ) )
        
        return [round(lx,4), round(ly,4)]

    def right_stick(self):
        """
        Gets the state of the right analog stick.

        Returns:
            The x & y axes as a tuple such that

            -1 <= x <= 1 && -1 <= y <= 1

            Negative values are left and down.
            Positive values are right and up.
        """
        rx = 0
        ry = 0
        
        self.refresh()
        
        if( self.connectStatus ): 
            rx = self.dead_zone_adjustment( self.joystick.get_axis( InputMap.RX ) )
            ry = self.dead_zone_adjustment( -self.joystick.get_axis( InputMap.RY ) )

        return [round(rx,4), round(ry,4)]
    