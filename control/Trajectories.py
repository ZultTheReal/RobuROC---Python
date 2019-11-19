import math as math

class Trajectories:

    def __init__(self):
        self.clear()

    def clear(self):
                                                                    # Settings
        self.pgoals = array[[0],[0]]                                # Trajectory goals
        self.goalCounter = 1                                        # Counter to select which goal to go to
        self.goalDistance = 0
        self.currentPosition = 0
        self.followTrajectory = 0

    def Trajectoryplanner(self, currentPosition):

        if self.followTrajectory == 1:
            temp = [0,0]
            temp[0] = self.pgoals[0][self.goalCounter]-currentPosition[0]
            temp[1] = self.pgoals[1][self.goalCounter]-currentPosition[1]
            self.goalDistance = math.sqrt(temp^2+temp^2)

            if self.goalDistance < 0.5:
                numcols = len(self.pgoals[0])
                if self.goalCounter <= len(numcols):
                    calculatedTrajectory = self.pgoals[:,self.goalCounter]
                    startTrajectory = self.pgoals[:,self.goalCounter-1]
                    self.goalCounter = self.goalCounter + 1
                    return startTrajectory, calculatedTrajectory
                else:
                    calculatedTrajectory = currentPosition
                    startTrajectory = self.pgoals[:, self.goalCounter - 1]
                    self.followTrajectory = 0
                    return startTrajectory, calculatedTrajectory
            else:
                startTrajectory = self.pgoals[:, self.goalCounter - 1]
                calculatedTrajectory = self.pgoals[:, self.goalCounter]
                return startTrajectory, calculatedTrajectory






