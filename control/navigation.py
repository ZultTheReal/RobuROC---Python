import math as math

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

        currentTrajectory = targetPosition - startPosition             #t

        if(abs(targetPosition[0])-currentPosition[0] <= self.deadzone and abs(targetPosition[1])-currentPosition[1] <= self.deadzone):  #if vehicle is close to goal, set error to 0 as to not move
            da = 0
            thetaError = 0
            return da, thetaError                            # NEEDS FIXING PLOX

        P = (startPosition+((((currentPosition-startPosition).transpose)*currentTrajectory)/((currentTrajectory.transpose)*currentTrajectory))*currentTrajectory)

        norm2trajectory = math.sqrt((trajectory ^ 2) + P ^ 2)
        if norm2trajectory <= self.l:
            da = norm2trajectory/self.ch
        else:
            da = self.k_d

        Pa = P + (da*currentTrajectory)/(math.sqrt(currentTrajectory ^ 2 + currentTrajectory^2))

        Poffset = Pa - currentPosition
        thetaRef = math.atan2(Poffset[1,0],Poffset[0,0])
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

