from joystick import Joystick

maxTrans = 5.0 # m/s
maxRot = 2.5 # m/s

gamepad = Joystick()


while(1):
    
    gamepad.run()
    
    left = round(gamepad.getForward() + gamepad.getRotate(),2)
    right = round(gamepad.getForward() - gamepad.getRotate(),2)
    
    print(left,right)