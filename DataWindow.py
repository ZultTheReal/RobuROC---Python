import ReceiveData as rd
from kivy.uix.screenmanager import ScreenManager, Screen

class DataScreen(Screen):
    def dataStarPeriodic(self):
        rd.startPeriodic(self)

    def dataStopPeriodic(self):
        rd.stopPeriodic(self)