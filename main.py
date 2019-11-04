
# Import the classes for interfacing with the RobuROC
import system as car
import control as con
import time

# Tell the Logging object where from to get the log data
car.log.addMeasurements(
    car.motors.actualCur,
    ['Current 1','Current 2','Current 3','Current 4']
)

car.log.addMeasurements(
    car.motors.actualVel,
    ['Velocity 1','Velocity 2','Velocity 3','Velocity 4']
)

#car.log.addMeasurements(
#    [gps.X, gps],
#    ['Heading','Latitude','Longitude','LinearSpeed']
#)



lastControl = 0

while( 1 ):
    
    car.gui.update()
    
    
    if car.var.loggingEnabled:
        car.log.update(0.01) # Log with 0.01s interval
    
    if time.time() - lastControl > .1:
        
        lastControl = time.time()
        
        left = 0.0
        right = 0.0
            
        # Control via xbox controller
        if car.var.gamepadEnabled:     
            if con.gamepad.buttons()[0]:

                # Get joystick values
                joystick = con.gamepad.left_stick()
                
                # Calculate left and right speed
                left = round(joystick[1] + joystick[0] / 4, 4)
                right = -round(joystick[1] - joystick[0] / 4, 4)

        # Else control via path finding
        
        car.motors.setSpeed( 0 , int(left * car.maxSpeed) )
        car.motors.setSpeed( 1 , int(right * car.maxSpeed) )
        car.motors.setSpeed( 2 , int(right * car.maxSpeed) )
        car.motors.setSpeed( 3 , int(left * car.maxSpeed) )
        
