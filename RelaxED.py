from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, TransitionBase

class ScreenManagement(ScreenManager):
    pass

class LoadingScreen(Screen):
    pass

class HomeScreen(Screen):
    pass

class ResourceScreen(Screen):
    pass

class QuoteScreen(Screen):
    pass


class TestApp(App):
    def build(self):
        self.fl = FloatLayout()
        return ScreenManagement()


TestApp().run()


