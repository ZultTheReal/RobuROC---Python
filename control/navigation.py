import math as math
import numpy as np
import utm
import json

from .optimalControl import OptimalControl

class Navigation:
    
    # Object for vehicle controller
    controller = OptimalControl()
    
    path = None # Trajectory goals
    endReached = True
    pathCount = 1  # Counter to select which goal to go to
    
    maxAimLen = 4.0  # Length from the point orthogonal to the route for which to aim
    minAimLen = 2.0  # Minimum length as to not slow down entirely
    deadzone = 4 # Deadzone, when the vehicle is within the radius of the target - change target.
    
    # Simpel P-controller gains (unitconversion)
    velGain = 0.4   # velGain * maxAimLen = maxSpeed
    rotGain = 1.0


    def __init__(self):
        self.reset()

    def reset(self):
        self.path = None
        self.pathCount = 1
        self.endReached = True
        
    def retry(self):
        self.endReached = False
        
    def setPath(self, path):
        self.path = path
        
        # Show the path on Google Map
        self.logToMap()
        
    def run(self, actualPos, actualHeading, actualVel, actualRot):
        
        # Use the pathfollower algorithm to calculate desired speeds for navigating
        velRef, rotRef = self.pathFollow(actualPos, actualHeading)

        # Map distance to linear speed, and map error in radians to rad/s
        velRef = self.velGain * velRef
        rotRef = self.rotGain * rotRef

        # Input to the controller
        return self.controller.run( velRef, rotRef, actualVel, actualRot)
        
        
    def pathFollow(self, actualPos, heading):
        
        # Convert lists to numpy arrays for easy vector calculations
        actualPos = np.array( actualPos )
        
        targetPos = np.array( self.path[self.pathCount] )
        startPos = np.array( self.path[self.pathCount-1] )
        
        # Calculate vector between target and actual postion to calculate the length
        target = targetPos - actualPos
        distance = math.sqrt( pow(target[0],2) + pow(target[1], 2))
        
        # If vehicle is close to targetPos, update the goal counter
        if(  abs(distance) <= self.deadzone ):
            
            # Check if there still are a new target
            if self.pathCount < (len(self.path) - 1):

                self.pathCount = self.pathCount + 1

            else:
                # Final goal reached, stop moving
                return 0, 0
        
        ###### Use Helmans method to calculate movement ######
        # Calculate vector between start and the target position (the wanted route)
        route = targetPos - startPos

        # Calculate the point which is orthorgonal to the route from the actualPos 
        orthPoint = startPos + ( ((actualPos - startPos) @ route)/(route @ route)) * route
        
        
        ###  Calculate the aiming point on the route ###
        
        # First calculate distance from orthPoint to targetPos
        orthRoute = targetPos - orthPoint
        distance = math.sqrt( pow(orthRoute[0],2) + pow(orthRoute[1], 2))
        
        # Depending on the distance, calculate the distance to next aim point
        if distance < self.maxAimLen:
            aimDistance = self.minAimLen if (distance < self.minAimLen) else distance
        else:
            aimDistance = self.maxAimLen


        ### Calculate the target heading for the vehicle ###
    
        # Calculate the lenght of the route
        routeLength = math.sqrt( pow(route[0],2) + pow(route[1], 2))
        
        # Calculate the aiming point by adding the route vector scaled by the aimDistance
        aimPoint = orthPoint + (aimDistance * route)/routeLength
    
        # Find the vector between actualPos and aimPoint
        aimRoute = aimPoint - actualPos

        # Calculate the angle of the aimRoute vector
        angle = math.atan2(aimRoute[1], aimRoute[0])
        
        # Map atan2 angle to two pi            
        thetaRef = (angle) % (2 * math.pi)
        
        # Find shortest route in degress  and map to radians
        thetaError = (thetaRef*180/math.pi - heading*180/math.pi + 540) % 360 - 180
        thetaError = thetaError*(math.pi/180)
    
        
        # Log the path-algorithm to Google Map
        # self.logToMap( actualPos, heading, orthPoint, aimPoint )
        
        return aimDistance, thetaError


    def logToMap(self, actualPos = None, heading = None, orthPoint = None, aimPoint = None):

        route = list()
        actual, orth, aim = None, None, None

        if self.path:
            for i in range(len(self.path)):
                route.append( utm.to_latlon(self.path[i][0], self.path[i][1], 32, 'V') )

        # Only log actual position if it is different than zero
        if actualPos and all(i != 0 for i in actualPos):
            actual = utm.to_latlon(actualPos[0], actualPos[1], 32, 'V')
        
        # Only add algorithm data if it is available
        if orthPoint and aimPoint:
            orth = utm.to_latlon(orthPoint[0], orthPoint[1], 32, 'V')
            aim = utm.to_latlon(aimPoint[0], aimPoint[1], 32, 'V')
    
        with open("map/pathlog.json", "w") as file:
            
            data = json.dumps({'route': route, 'actual':actual, 'orth':orth, 'aim': aim, 'heading': heading})
            file.write(data)
            