
# Import the classes for interfacing with the RobuROC
import system as car
import time

car.gui.gpsDataSource = car.gps.data

# Tell the Logging object where from to get the log data
car.log.addMeasurements(
    car.motors.actualCur,
    ['Current 1','Current 2','Current 3','Current 4']
)

car.log.addMeasurements(
    car.motors.actualVel,
    ['Velocity 1','Velocity 2','Velocity 3','Velocity 4']
)

car.log.addMeasurements(
    car.gps.data,
    ['Heading gps', 'Latitude', 'Lontitude', 'Speed', 'Sat. count']
)

car.log.addMeasurements(
    car.imu.data,
    ['gX', 'gY', 'gZ','aX', 'aY', 'aZ']
)

car.log.addMeasurements(
    car.compass.data,
    ['Heading mag', 'mX', 'mY']
)

#car.log.addMeasurements(
#    [gps.X, gps],
#    ['Heading','Latitude','Longitude','LinearSpeed']
#)



car.compass.connect('COM6')
car.gps.connect('COM13')
car.imu.connect('COM14')
    
lastControl = 0



while( car.gui.appOpen ):
    
    car.gui.update()
    
    car.gps.getData()
    car.imu.getData()
    car.compass.getData()
        
    if car.var.loggingEnabled:
        car.log.update(0.05) # Log with 0.01s interval
    
    if time.time() - lastControl > .1:

        lastControl = time.time()
        
        left = 0.0
        right = 0.0
            
        # Control via xbox controller
        if car.var.gamepadEnabled:     
            if car.gamepad.buttons()[0]: # If button A is pressed

                # Get joystick values
                joystick = car.gamepad.left_stick()
                
                # Calculate left and right speed
                left = round(joystick[1] + joystick[0] / 4, 4)
                right = -round(joystick[1] - joystick[0] / 4, 4)

        # Else control via path finding
        
        if car.motors.ready:
            car.motors.setRPM( 0 , left * car.maxSpeed )
            car.motors.setRPM( 1 , right * car.maxSpeed )
            car.motors.setRPM( 2 , right * car.maxSpeed )
            car.motors.setRPM( 3 , left * car.maxSpeed )
        
        #car.motors.setRPM( 0, 1.0 )
            
    # Print errors to gui log
    for i in range(0,len(car.errors)):

        error = car.errors.pop()
        #print(car.errors)
        car.gui.addToLog(error[0], error[1])

# If application is closed, kill the network
try:
    car.motors.disconnect()
except Exception as error:
    pass