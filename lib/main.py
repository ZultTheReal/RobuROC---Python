from xbox360_gamepad import Gamepad, XboxMap
import time

gamepad = Gamepad()

timer = 0

while(True):
    
    # Get all button states
    pressed = gamepad.buttons()

    # Get joystick values
    joystick = gamepad.left_stick()

    if time.time() - timer > 1/5: 
        timer = time.time()
        print( joystick )
        

    
    if not pressed[XboxMap.A]:
        # Set motor speeds to zero
        motorSpeed = [0, 0]

    # print(-lt[0], -lt[1])