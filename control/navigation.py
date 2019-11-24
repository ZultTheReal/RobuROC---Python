import math as math
import numpy as np
import utm
import json

from .optimalControl import OptimalControl

class Navigation:
    
    controller = OptimalControl()

    def __init__(self):
        self.clear()

    def clear(self):
                                                                    # Settings
        self.pgoals = list()                               # Trajectory goals
        self.goalCounter = 1                                        # Counter to select which goal to go to
        self.goalDistance = 0
        self.actualPos = 0
        self.followTrajectory = 1
        
        
        self.maxAimLen = 2
        self.minLen = 4 # Begin slowing down at this distance to aim point
        self.aimLenFactor = self.minLen/self.maxAimLen
        self.deadzone = 0.2
        
    def run(self, actualPosition, actualHeading, actualVel, actualRot):
        
        startPos, nextPosition = self.pathPlanner(actualPostion)
        
        velRef, rotRef = self.pathFollow(nextPosition, actualPosition, startPos, actualHeading)
        
        # Input to the controller
        return self.controller.run( velRef, rotRef, actualVel, actualRot)
        
        
    def pathFollow(self, startPos, targetPos, actualPos, heading):
        
        # Convert lists to numpy arrays for easy vector calculations
        targetPos = np.array(targetPos)
        actualPos = np.array(actualPos)
        startPos = np.array(startPos)
        
        #print("TARGET",targetPos)
        #print("ACTUAL",actualPos)
        #print("START",startPos)
        
        # Calculate vector between target and actual postion to calculate the length
        target = targetPos - actualPos
        distance = math.sqrt( pow(target[0],2) + pow(target[1], 2))
        
        # If vehicle is close to targetPos, return outputs as zero
        if(  abs(distance) <= self.deadzone ):  
            return 0, 0
        
        # If not, use Helmans method to calculate movement
        else:
            
            # Calculate vector between start and the target position (the wanted route)
            route = targetPos - startPos

            # Calculate the point which is orthorgonal to the route from the actualPos 
            orthPoint = startPos + ( ((actualPos - startPos) @ route)/(route @ route)) * route
            
            
            # --- Calculate the aiming point on the route ---
            
            # First calculate distance from orthPoint to targetPos
            orthRoute = targetPos - orthPoint
            distance = math.sqrt( pow(orthRoute[0],2) + pow(orthRoute[1], 2))
            
            # Depending on the distance, calculate the distance to next aim point
            if distance <= self.minLen:
                aimDistance = distance/self.aimLenFactor
            else:
                aimDistance = self.maxAimLen

            # Calculate the lenght of the route
            routeLength = math.sqrt( pow(route[0],2) + pow(route[1], 2))
            
            # Calculate the aiming point by adding the route vector scaled by the aimDistance
            aimPoint = orthPoint + (aimDistance * route)/routeLength
            

            # --- Calculate the target heading for the vehicle ---
        
            # First find the vector between actualPos and aimPoint
            aimRoute = aimPoint - actualPos

            # Calculate the angle of the aimRoute vector
            #thetaRef = self.atan360(aimRoute[1], aimRoute[0])
            
            angle = math.atan2(aimRoute[1], aimRoute[0])
            
            #print("aimRoute", aimRoute )
                        
            thetaRef = (angle) % (2 * math.pi)
        
            
            #print("thetaRef", thetaRef)
            #print(thetaRef)
            
            # Find the error in the vehicle heading 
            #thetaError = thetaRef - heading
            
            # Find shortest route in degress 
            thetaError = (thetaRef*180/math.pi - heading*180/math.pi + 540) % 360 - 180
            thetaError = thetaError*(math.pi/180)
            
            print("thetaError", thetaError)
            
            with open("map/pathlog.json", "w") as file:
                
                start = utm.to_latlon(startPos[0], startPos[1], 32, 'V')
                target = utm.to_latlon(targetPos[0], targetPos[1], 32, 'V')
                actual = utm.to_latlon(actualPos[0], actualPos[1], 32, 'V')
                orth = utm.to_latlon(orthPoint[0], orthPoint[1], 32, 'V')
                aim = utm.to_latlon(aimPoint[0], aimPoint[1], 32, 'V')
                
                data = json.dumps({'start': start, 'target': target, 'actual':actual, 'orth':orth, 'aim': aim, 'heading': heading})
                file.write(data)
            

            return aimDistance, thetaError

    def pathPlanner(self, actualPos):

        if self.followTrajectory == 1:
            temp = [0,0]
            temp[0] = self.pgoals[0][self.goalCounter]-actualPos[0]
            temp[1] = self.pgoals[1][self.goalCounter]-actualPos[1]
            self.goalDistance = math.sqrt(temp^2+temp^2)

            if self.goalDistance < 0.5:
                numcols = len(self.pgoals[0])
                
                if self.goalCounter <= numcols:
                    
                    nextPosition = self.pgoals[self.goalCounter]
                    startPos = self.pgoals[self.goalCounter-1]
                    self.goalCounter = self.goalCounter + 1
                    return startPos, nextPosition
                
                else:
                    
                    nextPosition = actualPos
                    startPos = self.pgoals[self.goalCounter - 1]
                    self.followTrajectory = 0
                    return startPos, nextPosition
                
            else:
                
                startPos = self.pgoals[self.goalCounter - 1]
                nextPosition = self.pgoals[self.goalCounter]
                return startPos, nextPosition


    # Atan2, but with output from 0 to 2*pi instead
    def atan360(self, x,y):
        
        angle = math.atan2(x,y)
        
        if angle < 0:
            angle = angle + 2 * math.pi

        return angle


#nav = Navigation()

#utm1 = utm.from_latlon(57.014358, 9.986570)
#utm2 = utm.from_latlon(57.014309, 9.986611)
#utm3 = utm.from_latlon(57.014287, 9.987066)

#startPos = [utm1[0], utm1[1]]
#actualPos = [utm2[0], utm2[1]]
#targetPos = [utm3[0], utm3[1]]

#targetPos = [5, 10.5]
#startPos = [2,3]
#actualPos = [7.5,3.5]
#heading = math.pi/2

#print( nav.pathFollow( startPos, targetPos, actualPos, heading ) )

#print( math.atan2(0.5,-4) * 180/math.pi )

#targetAngle = 280
#currentAngle = -80
#test = (targetAngle - currentAngle + 540) % 360 - 180

#print(test)



#print( atan360(-0.5, -4)*180/math.pi )

