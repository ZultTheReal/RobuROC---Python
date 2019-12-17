
# Import the classes for interfacing with the RobuROC
import system as car
import control as con
import time
import math
import utm
#import httpServer

from threading import Thread

initKalman = [False]

path = list()

#path.append([559998.14, 6319386.08])
#path.append([560032.37, 6319383.35])
#path.append([560032.37, 6319368.05])
#path.append([559998.14, 6319368.05])
#path.append([559998.14, 6319386.08])


#path.append([560014, 6319384])
#path.append([560034, 6319384])
#path.append([560034, 6319359])
#path.append([560014, 6319359])
#path.append([560014, 6319384])

#path.append([559705, 6319173.31])
#path.append([559743, 6319173.31])
#path.append([559743, 6319193.31])
#path.append([559705, 6319193.31])
#path.append([559705, 6319173.31])

path.append([559705, 6319253.15])
path.append([559705, 6319233.15])
path.append([559748.5, 6319233.15])
path.append([559748.5, 6319213.15])
path.append([559705, 6319213.15])
path.append([559705, 6319233.15])
path.append([559748.5, 6319233.15])
path.append([559748.5, 6319253.15])
path.append([559705, 6319253.15])

con.navigation.setPath(path)

car.gui.setPathSource(path)
car.gui.setGpsSource(car.gps.data)
car.gui.setGyroSource(car.imu.data)


otherData = [0]


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
    ['Heading gps', 'Latitude', 'Lontitude', 'Speed', 'LPF speed']
)

car.log.addMeasurements(
    car.imu.data,
    ['gX', 'gY', 'gZ']
)


car.log.addMeasurements(
    con.EKF.data,
    ['EKF_X','EKF_Y', 'EKF_Theta', 'EKF_Vb', 'EKF_Omega', 'EKF_Sl', 'EKF_Sr', 'Sl_sensor', 'Sr_sensor']
)

car.log.addMeasurements(
    con.navigation.controller.data,
    ['Ref_l','Ref_r']
)


car.log.addMeasurements(
    car.compass.data,
    ['Heading mag', 'mX', 'mY']
)

car.log.addMeasurements(
    car.gps.utmData,
    ['Easting', 'Northing']
)

car.log.addMeasurements(
    otherData,
    ['GPS Available']
)

car.compass.connect('COM6')
car.gps.connect('COM13')
car.imu.connect('COM14')

car.gps.readData() # remeber that this should run untill first gps posistion
car.imu.getData()
car.compass.getData()

counterButton = [0]

# Function to run at control loop speed
def excecuteControl():
    
    left = 0.0
    right = 0.0
    
    # Inputdata for Kalman
    gpsPos, gpsSpeed, dataStatus = car.gps.getNewestData()
    
    otherData[0] = dataStatus
    
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
            
            counterButton[0] = 0

            if( car.gps.sat_count >= 0):
                
                if not initKalman[0]:
                    initKalman[0] = True
                    con.EKF.set_Init(gpsPos[0],gpsPos[1],car.compass.heading) #init kalman with x, y and theta
                else:
                
                    leftWheel = (car.motors.actualVel[0] + car.motors.actualVel[3])/(2*car.WHEEL_RADIUS)
                    rightWheel = (car.motors.actualVel[1] + car.motors.actualVel[2])/(2*car.WHEEL_RADIUS)

 
                    con.EKF.updateEKF(leftWheel, rightWheel, gpsPos[0], gpsPos[1], car.gps.heading, car.compass.heading, gpsSpeed, car.imu.gz, dataStatus)
                    speed = con.navigation.run(gpsPos, car.compass.heading, float(con.EKF.mu[3]), float(con.EKF.mu[4]))

                    

                    # Test step-response
                    #velRef = 1 # m/s
                    #rotRef = 0.5 # rad/s
                    #speed = con.navigation.controller.run(velRef, rotRef, float(con.EKF.mu[3]), float(con.EKF.mu[4]))
                    
                    #slipGainL = 1/(1-float(con.EKF.mu[5]))
                    #slipGainR = 1/(1-float(con.EKF.mu[6])) 

                    #print(slipGainL, slipGainR)
                     
                    #speed[0] = (speed[0] * slipGainL) if con.EKF.mu[5] < 0.4 else speed[0] * 1/0.6
                    #speed[1] = (speed[1] * slipGainR) if con.EKF.mu[6] < 0.4 else speed[1] * 1/0.6

                    if car.motors.ready:
                        car.motors.setRPS( 0 , speed[0])
                        car.motors.setRPS( 1 , -speed[1])
                        car.motors.setRPS( 2 , -speed[1])
                        car.motors.setRPS( 3 , speed[0])
                
        else:      

            counterButton[0] = counterButton[0] + 1

            if(counterButton[0] > 20 ): 
                if initKalman[0]:
                    print("DU SLAP (B) DIN ABEKAT!!")
                
                initKalman[0] = False
            
  
                if car.motors.ready:
                    car.motors.setCurrent( 0 , 0)
                    car.motors.setCurrent( 1 , 0 )
                    car.motors.setCurrent( 2 , 0 )
                    car.motors.setCurrent( 3 , 0 )

def getSensorData():
    while(1):
        car.gps.readData()
        car.imu.getData()
        car.compass.getData()
        
thread = Thread(target = getSensorData)
thread.start()

toggleLog = False

while( car.gui.appOpen ):
    
    start_time = time.time()
    
    if car.var.gamepadEnabled:
        if car.gamepad.buttons()[2]: # If button A is pressed
            if not toggleLog:
                if car.var.loggingEnabled:
                    print("Not logging")
                    car.var.loggingEnabled = False
                    car.log.stop()
                else:
                    print("Logging")
                    car.var.loggingEnabled = True
                    car.log.begin()
                toggleLog = True
                
                
            
        else:
            toggleLog = False

     # Log with the frequency the function is called
    if car.var.loggingEnabled:
        car.log.addLine()
    
    car.gui.update()

    excecuteControl()

    cpu_usage = ((time.time() - start_time)/0.025)*100
    if cpu_usage > 100:
        print("CPU-TIME:", round(cpu_usage,2) )
    
    excecution_time = time.time() - start_time
    
    if excecution_time < 0.025:
        # Sleep the 
        time.sleep(0.025 - (time.time() % 0.025))
    
        
    # Print errors to gui log
    for i in range(0,len(car.errors)):

        error = car.errors.pop()
        #print(car.errors)
        car.gui.addToLog(error[0], error[1])


# If application is closed, kill the network and stop control timer
car.motors.disconnect()
continueControl = False