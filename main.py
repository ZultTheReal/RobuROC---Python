
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


con.navigation.pgoals = path

car.gui.pathSource = path

#utm1 = utm.from_latlon(57.014354, 9.986582)
#utm2 = utm.from_latlon(57.014296, 9.986608)
#utm3 = utm.from_latlon(57.014284, 9.987197)

#startPos = [utm1[0], utm1[1]]
#actualPos = [utm2[0], utm2[1]]
#targetPos = [utm3[0], utm3[1]]
#heading = 90.0

#while(1):

 #   actualPos[0] += random.randint(-10,100)/200.0
  #  actualPos[1] += random.randint(-10,50)/200.0
   # con.navigation.pathFollow(startPos, targetPos, actualPos, heading )
   # time.sleep(0.5)

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

car.log.addMeasurements(
    car.gps.utmData,
    ['Easting', 'Northing']
)

car.compass.connect('COM6')
car.gps.connect('COM13')
car.imu.connect('COM14')
    
lastControl = 0

#car.gps.latitude = 57.014359
#car.gps.longitude = 9.986557
#print("SHIT",utm.from_latlon( car.gps.latitude, car.gps.longitude ))
                    
while( car.gui.appOpen ):
    
    car.gui.update()
    
    car.gps.getData()
    car.imu.getData()
    car.compass.getData()
        
    if car.var.loggingEnabled:
        car.log.update(0.05) # Log with 0.01s interval
    
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
                                       
                        speed = con.navigation.run(actualPos, car.compass.heading, car.gps.superSpeed, car.imu.gz)

                        #speed = con.navigation.controller.run(velRef, rotRef, actualVel, actualRot) # 0.5, 0.10, car.gps.superspe
                    
                    #print("Heading: ", car.compass.heading )
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
        
        car.gps.latitude = 57.014359
        car.gps.longitude = 9.986557
        
        # Sample GPS start position
        start = car.gps.getUTM()
        
        # Insert the start position as start coordinate in the path list
        path.insert(0, [start[0], start[1]]) # Northing, Easting
        
        #print(path)
        

# If application is closed, kill the network
try:
    car.motors.disconnect()
except Exception as error:
    pass