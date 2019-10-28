from tkinter import *
from tkinter import ttk
import ApplicationSetup as apps
import StateCommands as sc
import ReceiveData as rd
import Functions as f
import Variables as var

def close():
    sc.disableVoltage()
    rd.stopPeriodic()
    if var.logging:
        var.logging = False
        #var.currentMeasurements.close()
        #var.velocityMeasurements.close()
        #var.positionMeasurements.close()
        #var.directionMeasurements.close()
        var.combinedMeasurements.close()
    var.appOpen = False
    apps.app.destroy()

def egnition():
    rd.stopPeriodic()
    sc.reset()
    sc.enable()
    var.driveReady = True
    rd.startPeriodic()

def disable():
    sc.disableVoltage()
    var.driveReady = False

def setSpeed():
    var.maxSpeed = int(apps.manualSpeed.get())


