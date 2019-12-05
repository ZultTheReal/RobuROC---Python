
# Import the classes for interfacing with the RobuROC
import system as car
import control as con
import time
import math

#import httpServer
import utm

import random


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


    
lastControl = 0

#car.gps.latitude = 57.014359
#car.gps.longitude = 9.986557
#print("SHIT",utm.from_latlon( car.gps.latitude, car.gps.longitude ))
                    
while( car.gui.appOpen ):
    
    car.gui.update()
    
    gpsAvailble = car.gps.getData()
    car.imu.getData()
    car.compass.getData()
        
    if car.var.loggingEnabled:
        car.log.update(0.01) # Log with 0.01s interval
    
    if time.time() - lastControl > .05:

        # Calculate actual velocity

        #actualSpeed = (car.motors.actualVel[0] + car.motors.actualVel[1])/2
        #print( "ACTUAL: ", car.motors.actualVel[0], car.motors.actualVel[1] )

        #print(car.imu.gz)

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
                #car.motors.setMPS(1, 0.5)
                #print("ACTUAL", car.motors.actualVel[0], car.motors.actualVel[1])
                #print( -car.imu.gz )
                
                if( car.gps.sat_count >= 0):
                    
                    #car.gps.latitude = 57.014359
                    #car.gps.longitude = 9.986557
                    #car.gps.superSpeed = 1.0
                    
                    if car.gamepad.buttons()[1]:
                    
                        actualPos = car.gps.getUTM()
                        con.EKF.updateEKF((car.motors.actualVel[0] + car.motors.actualVel[3])/(2*car.WHEEL_RADIUS),
                                           (car.motors.actualVel[1] + car.motors.actualVel[2])/(2*car.WHEEL_RADIUS),
                                              actualPos[0], actualPos[1], car.compass.heading, #angle to be replaced with gps angle
                                              car.compass.heading, car.gps.linear_speed, car.imu.gz, gpsAvailble)
                                       
                        #speed = con.navigation.run(actualPos, car.compass.heading, car.gps.superSpeed, car.imu.gz)
                         
                        # Test step-response
                        velRef = 1 # m/s
                        rotRef = 0 # rad/s
                        speed = con.navigation.controller.run(velRef, rotRef, float(con.EKF.mu[3]), float(con.EKF.mu[4]))
                        #print("GPS:", gpsAvailble)
                        #print("EKF SPEED: ", con.EKF.mu[3])
                        #print("EKF ANG SPEED: ", con.EKF.mu[4])
                        #print("SL and SR: ", con.EKF.mu[5], con.EKF.mu[6])
                        #print("wheel sppeed", car.motors.actualVel)
                        #print("Data EKF: " ,con.EKF.data)
                        #print("Data GPS: " ,car.gps.data)
                        #speed = con.navigation.controller.run(velRef, rotRef, actualVel, actualRot) # 0.5, 0.10, car.gps.superspe
                    
                        #print("Omega: ", car.imu.gz )
                        #print("Velocity: ", car.gps.superSpeed )
                    #print("N: ", path[1][0] - actualPos[0])
                    #print("E: ", path[1][1] - actualPos[1])
                
                    #velRef, rotRef = con.navigation.pathFollow(path[0], path[1], actualPos, car.compass.heading )
                    
                    #velRef = 0.3 * velRef
                    #rotRef = -0.2 * rotRef
                    
                    #speed = con.navigation.controller.run( velRef, rotRef, car.gps.superSpeed, car.imu.gz) # 0.5, 0.10, car.gps.superspeed, -car.imu.gz

                    if car.motors.ready:
                        car.motors.setRPS( 0 , speed[0])
                        car.motors.setRPS( 1 , -speed[1])
                        car.motors.setRPS( 2 , -speed[1])
                        car.motors.setRPS( 3 , speed[0])
                        
            else:
                if car.motors.ready:
                    car.motors.setCurrent( 0 , 0)
                    car.motors.setCurrent( 1 , 0 )
                    car.motors.setCurrent( 2 , 0 )
                    car.motors.setCurrent( 3 , 0 )
                    
    # Print errors to gui log
    for i in range(0,len(car.errors)):

        error = car.errors.pop()
        #print(car.errors)
        car.gui.addToLog(error[0], error[1])
        
    if car.var.startFollowPath:
        
        car.var.startFollowPath = False
  
        # Sample GPS start position
        start = car.gps.getUTM()
        
        # Insert the start position as start coordinate in the path list
        path.insert(0, [start[0], start[1]]) # Northing, Easting
        

# If application is closed, kill the network
car.motors.disconnect()
