#  Copyright Emil Jacobsen (SolidGeek)
#
#  This is a heavily simplified/modified version of joncoop's pygame-xbox360controller
#
#      <https://github.com/joncoop/pygame-xbox360controller>.


import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
import time

LINUX = 0
WINDOWS = 1

if sys.platform.startswith("lin"):
    platform_id = LINUX
elif sys.platform.startswith("win"):
    platform_id = WINDOWS

if platform_id == LINUX:
    class XboxMap:
        # Digital inputs (buttons)
        A = 0 # Button A
        B = 1 # Button B
        X = 2 # Button X
        Y = 3 # Button Y
        LB = 4 # Button LB
        RB = 5 # Button RB
        BACK = 6 # Button BACK
        START = 7 # Button START
        LS = 9 # Left stick button
        RS = 10 # Right stick button
        
        # Analog inputs (axis)
        LX = 0 # Left stick x
        LY = 1 # Left stick y
        LT = 2 # Left trigger 
        RX = 3 # Rigth stick x
        RY = 4 # Rigth stick y
        RT = 5 # Right trigger 

elif platform_id == WINDOWS:
    class XboxMap:
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

class Gamepad:
    
    joystick = None
    joystick_id = 0
    connectStatus = False
    refresh_time = 0 
    refresh_delay = 0

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
        
        count = pygame.joystick.get_count()

        if( count >= 1 ):
            # Select the first joystick in the array
            self.joystick = pygame.joystick.Joystick(self.joystick_id)
            self.joystick.init()
        
        self.refresh()

    def refresh(self):
        if self.refresh_time < time.time():
            
            # Define next refresh time
            self.refresh_time = time.time() + self.refresh_delay
            
            # Reinitiaze the joystick instance in the pygame object to get current joystick count - takes zero time
            pygame.joystick.quit()
            pygame.joystick.init()
            
            count = pygame.joystick.get_count()
 
            if( count >= 1 ):
                self.joystick = pygame.joystick.Joystick(self.joystick_id)
                self.joystick.init()
                
                if not self.connectStatus:
                    self.connectStatus = True
                    print('Joystick was connected')
            else:
                if self.connectStatus:
                    self.connectStatus = False
                    print('Joystick was disconnected')
                
                
            # Read pygame events (needed to read joystick), return the events for debugging purposes
            return pygame.event.get()

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
                self.joystick.get_button( XboxMap.A ), 
                self.joystick.get_button( XboxMap.B ),
                self.joystick.get_button( XboxMap.X ),
                self.joystick.get_button( XboxMap.Y ),
                self.joystick.get_button( XboxMap.LB ),
                self.joystick.get_button( XboxMap.RB ),
                self.joystick.get_button( XboxMap.LS ),
                self.joystick.get_button( XboxMap.RS ),
                self.joystick.get_button( XboxMap.BACK ),
                self.joystick.get_button( XboxMap.START ),
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
            lx = self.dead_zone_adjustment( self.joystick.get_axis( XboxMap.LX ) )
            ly = self.dead_zone_adjustment( -self.joystick.get_axis( XboxMap.LY ) )
        
        return {'x':round(lx,4), 'y':round(ly,4)}

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
            rx = self.dead_zone_adjustment( self.joystick.get_axis( XboxMap.RX ) )
            ry = self.dead_zone_adjustment( -self.joystick.get_axis( XboxMap.RY ) )

        return {'x':round(rx,4), 'y':round(ry,4)}
    