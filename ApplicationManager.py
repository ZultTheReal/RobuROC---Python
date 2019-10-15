from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

    def do_layout(self, *args, **kwargs):
        super(WindowManager, self).do_layout()
        width, height = Window.size
        if width < 800:
            Window.size = 800, Window.size[1]
        if height < 480:
            Window.size = Window.size[0], 480
