from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

    def do_layout(self, *args, **kwargs):
        super(WindowManager, self).do_layout()
        Window.borderless = True
        Window.maximize()
        Window.size = 800, 480
