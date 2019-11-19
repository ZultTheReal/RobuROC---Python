import numpy as np
import math as math

class PathFollowing:

    def __init__(self):
        self.clear()

    def clear(self):
        self.ch = 8
        self.k_d = 2
        self.l = 16
        self.deadzone = 0.2


    def PathFollowingController(self,trajectory,positionData,Pstart,angleData):

        currentTrajectory = trajectory - Pstart             #t

        if(abs(trajectory[0])-positionData[0] <= self.deadzone and abs(trajectory[1])-positionData[1] <= self.deadzone):  #if vehicle is close to goal, set error to 0 as to not move
            da = 0
            thetaError = 0
            return da, thetaError                            # NEEDS FIXING PLOX

        P = (Pstart+((((positionData-Pstart).transpose)*currentTrajectory)/((currentTrajectory.transpose)*currentTrajectory))*currentTrajectory)

        norm2trajectory = math.sqrt((trajectory ^ 2) + P ^ 2)
        if norm2trajectory <= self.l:
            da = norm2trajectory/self.ch
        else:
            da = self.k_d

        Pa = P + (da*currentTrajectory)/(math.sqrt(currentTrajectory ^ 2 + currentTrajectory^2))

        Poffset = Pa - positionData
        thetaRef = math.atan2(Poffset[1,0],Poffset[0,0])
        thetaError = thetaRef - angleData

        return da,thetaError