import StateCommands
import MovementCommands
from MovementCommands import *
from StateCommands import *
from kivy.uix.screenmanager import ScreenManager, Screen

class MainScreen(Screen):

    def mwForward(self):
        forward(self)

    def mwBackward(self):
        backward(self)

    def mwLeft(self):
        moveLeft(self)

    def mwRight(self):
        moveRight(self)

    def mwStop(self):
        holdStill(self)

    def mwmanualSpeed(self):
        convert_manualspeed(self.manualspeed.text)

    def mwsetSpeed1(self):
        setSpeed1(self)

    def mwsetSpeed2(self):
        setSpeed2(self)

    def mwsetSpeed3(self):
        setSpeed3(self)

    def mwsetSpeed4(self):
        setSpeed4(self)

    def mwsetSpeedAll(self):
        setSpeedAll(self)

    def mwReset(self):
        reset()

    def mwQuickStop(self):
        quickStop()

    def mwEnable(self):
        enable()

    def mwDisableVoltage(self):
        disableVoltage()

    def mwShutDown(self):
        shutDown()