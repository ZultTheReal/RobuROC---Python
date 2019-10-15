import StateCommands as sc
import MovementCommands as mc
from kivy.uix.screenmanager import ScreenManager, Screen

class MainScreen(Screen):

    def mwForward(self):
        mc.forward(self)

    def mwBackward(self):
        mc.backward(self)

    def mwLeft(self):
        mc.moveLeft(self)

    def mwRight(self):
        mc.moveRight(self)

    def mwStop(self):
        mc.holdStill(self)

    def mwsetSpeed1(self):
        mc.setSpeed1(self)

    def mwsetSpeed2(self):
        mc.setSpeed2(self)

    def mwsetSpeed3(self):
        mc.setSpeed3(self)

    def mwsetSpeed4(self):
        mc.setSpeed4(self)

    def mwsetSpeedAll(self):
        mc.setSpeedAll(self)

    def mwReset(self):
        sc.reset()

    def mwQuickStop(self):
        sc.quickStop()

    def mwEnable(self):
        sc.enable()

    def mwDisableVoltage(self):
        sc.disableVoltage()

    def mwShutDown(self):
        sc.shutDown()