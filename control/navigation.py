import math as math
import numpy as np

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
        self.currentPosition = 0
        self.followTrajectory = 1
        
        self.ch = 8
        self.k_d = 2
        self.l = 16
        self.deadzone = 0.2
        
    def run(self, actualPosition, actualHeading, actualVel, actualRot):
        
        startPosition, nextPosition = self.pathPlanner(actualPostion)
        
        velRef, rotRef = self.pathFollow(nextPosition, actualPosition, startPosition, actualHeading)
        
        # Input to the controller
        return self.controller.run( velRef, rotRef, actualVel, actualRot)
        
        
    def pathFollow(self, targetPosition, currentPosition, startPosition, angle):

        targetPosition = np.array(targetPosition)
        currentPosition = np.array(currentPosition)
        startPosition = np.array(startPosition)

        currentTrajectory = targetPosition - startPosition             #t


        if(abs(targetPosition[0])-currentPosition[0] <= self.deadzone and abs(targetPosition[1])-currentPosition[1] <= self.deadzone):  #if vehicle is close to goal, set error to 0 as to not move
            da = 0
            thetaError = 0
            return da, thetaError                            # NEEDS FIXING PLOX

        t1 = (currentPosition-startPosition) @ currentTrajectory
        t2 = (currentTrajectory @ currentTrajectory)
    
        P = startPosition + ( t1 / t2) * currentTrajectory
        
        vectorLength = targetPosition - P
        norm2trajectory = math.sqrt( pow(vectorLength[0],2) + pow(vectorLength[1], 2))
        
        
        if norm2trajectory <= self.l:
            da = norm2trajectory/self.ch
        else:
            da = self.k_d

        norm2t = math.sqrt( pow(currentTrajectory[0],2) + pow(currentTrajectory[1], 2))

        Pa = P + (da * currentTrajectory)/norm2t

        Poffset = Pa - currentPosition
        thetaRef = math.atan2(Poffset[1],Poffset[0])
        thetaError = thetaRef - angle

        return da, thetaError

    def pathPlanner(self, currentPosition):

        if self.followTrajectory == 1:
            temp = [0,0]
            temp[0] = self.pgoals[0][self.goalCounter]-currentPosition[0]
            temp[1] = self.pgoals[1][self.goalCounter]-currentPosition[1]
            self.goalDistance = math.sqrt(temp^2+temp^2)

            if self.goalDistance < 0.5:
                numcols = len(self.pgoals[0])
                
                if self.goalCounter <= numcols:
                    
                    nextPosition = self.pgoals[self.goalCounter]
                    startPosition = self.pgoals[self.goalCounter-1]
                    self.goalCounter = self.goalCounter + 1
                    return startPosition, nextPosition
                
                else:
                    
                    nextPosition = currentPosition
                    startPosition = self.pgoals[self.goalCounter - 1]
                    self.followTrajectory = 0
                    return startPosition, nextPosition
                
            else:
                
                startPosition = self.pgoals[self.goalCounter - 1]
                nextPosition = self.pgoals[self.goalCounter]
                return startPosition, nextPosition


#nav = Navigation()

#startPos = [559947.54, 6319407.73]
#actualPos = [559950.54, 6319410.73]
#targetPos = [559980.54, 6319450.73]


#print( nav.pathFollow( targetPos, actualPos, startPos, 180.0*math.pi/180) )