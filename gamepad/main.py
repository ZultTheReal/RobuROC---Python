from xbox360_gamepad import Gamepad, XboxMap

gamepad = Gamepad()

while(True):

    # Get all button states
    pressed = gamepad.buttons()
    
    # Get joystick values
    joystick = gamepad.left_stick()
    print( joystick )
    
    
    if not pressed[XboxMap.A]:
        # Set motor speeds to zero
        motorSpeed = [0, 0]

    # print(-lt[0], -lt[1])