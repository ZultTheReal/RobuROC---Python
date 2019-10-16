import ReceiveData
from kivy.uix.screenmanager import ScreenManager, Screen

class DataScreen(Screen):
    def dataStarPeriodic(self):
        ReceiveData.startPeriodic(self)

    def dataStopPeriodic(self):
        ReceiveData.stopPeriodic(self)