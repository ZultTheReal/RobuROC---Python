
# Import the classes for interfacing with the RobuROC
import system as car
import control as con
import time
import math
import utm
#import httpServer

from threading import Timer

continueControl = True;


# Function for running the control system
def repeater(start, interval, count):   
    # Get current time
    ticks = time.time()
    
    # Set next timing event
    t = Timer( interval - (ticks-start-count*interval), repeater, [start, interval, count+1])
    t.start()
    print(ticks - start, "#", count )
    
    # Perform function here
    excecuteControl();
    
    if not continueControl:
        t.cancel()
    
dt = 0.025 # interval in sec
t = Timer(dt, repeater, [round(time.time()), dt, 0]) # start over at full second, round only for testing here
t.start()


path = list()

path.append([559998.14, 6319386.08])
path.append([560032.37, 6319383.35])
path.append([560032.37, 6319368.05])
path.append([559998.14, 6319368.05])
path.append([559998.14, 6319386.08])


con.navigation.setPath(path)

car.gui.setPathSource(path)
car.gui.setGpsSource(car.gps.data)


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
    con.EKF.data,
    ['EKF_X','EKF_Y', 'EKF_Theta', 'EKF_Vb', 'EKF_Omega', 'EKF_Sl', 'EKF_Sr']
)

car.log.addMeasurements(
    con.navigation.controller.data,
    ['Ref_l','Ref_r']
    )


#car.log.addMeasurements(
#    car.compass.data,
#    ['Heading mag', 'mX', 'mY']
#)

#car.log.addMeasurements(
#    car.gps.utmData,
#    ['Easting', 'Northing']
#)

car.compass.connect('COM6')
car.gps.connect('COM13')
car.imu.connect('COM14')

gpsAvailble = car.gps.getData() # remeber that this should run untill first gps posistion
car.imu.getData()
car.compass.getData()
actualPos = car.gps.getUTM()

con.EKF.set_Init(actualPos[0],actualPos[1],car.compass.heading) #init kalman with x, y and theta


# Function to run at control loop speed
def excecuteControl():
    
    left = 0.0
    right = 0.0

        
    # Control via xbox controller
    if car.var.gamepadEnabled:
        if car.gamepad.buttons()[0]: # If button A is pressed

            # Get joystick values
            joystick = car.gamepad.left_stick()
            
            # Calculate left and right speed
            left = round(joystick[1] + joystick[0] / 4, 4)
            right = round(joystick[1] - joystick[0] / 4, 4)

            left = left * car.maxSpeed
            right = right * car.maxSpeed
            
            if car.motors.ready:
                car.motors.setMPS( 0 , left)
                car.motors.setMPS( 1 , -right )
                car.motors.setMPS( 2 , -right )
                car.motors.setMPS( 3 , left )

        # Else control via path finding
        elif car.gamepad.buttons()[1]:
            
            if( car.gps.sat_count >= 0):

                # Inputdata for Kalman
                actualPos = car.gps.getUTM()
                leftWheel = (car.motors.actualVel[0] + car.motors.actualVel[3])/(2*car.WHEEL_RADIUS);
                rightWheel = (car.motors.actualVel[1] + car.motors.actualVel[2])/(2*car.WHEEL_RADIUS);
                
                con.EKF.updateEKF(leftWheel,rightWheel,actualPos[0], actualPos[1], car.compass.heading, car.compass.heading, car.gps.linear_speed, car.imu.gz, gpsAvailble)
                               
                #speed = con.navigation.run(actualPos, car.compass.heading, car.gps.superSpeed, car.imu.gz)
                 
                # Test step-response
                velRef = 1 # m/s
                rotRef = 0 # rad/s
                speed = con.navigation.controller.run(velRef, rotRef, float(con.EKF.mu[3]), float(con.EKF.mu[4]))
                    
        else:
            if car.motors.ready:
                car.motors.setCurrent( 0 , 0)
                car.motors.setCurrent( 1 , 0 )
                car.motors.setCurrent( 2 , 0 )
                car.motors.setCurrent( 3 , 0 )
    
    if car.var.loggingEnabled:
        car.log.addLine() # Log with the frequency the function is called

                    
while( car.gui.appOpen ):
    
    car.gui.update()
    
    gpsAvailble = car.gps.getData()
    car.imu.getData()
    car.compass.getData()
        
    # Print errors to gui log
    for i in range(0,len(car.errors)):

        error = car.errors.pop()
        #print(car.errors)
        car.gui.addToLog(error[0], error[1])


# If application is closed, kill the network and stop control timer
car.motors.disconnect()
continueControl = False