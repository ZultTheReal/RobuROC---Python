from tkinter import *
from tkinter import ttk
import ApplicationSetup as apps
import StateCommands as sc
import ReceiveData as rd
import Functions as f
import Variables as var

def close():
    apps.app.destroy()
    sc.disableVoltage()
    rd.stopPeriodic()
    f.stopLogging()

def egnition():
    sc.reset()
    sc.enable()
    rd.startPeriodic()
    var.driveReady = True

def disable():
    sc.disableVoltage()
    rd.stopPeriodic()
    var.driveReady = False

def setSpeed():
    var.maxSpeed = int(apps.manualSpeed.get())


