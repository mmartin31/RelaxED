from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, TransitionBase
from kivy.core.window import Window

class ScreenManagement(ScreenManager):
    pass


class LoadingScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, dt):
        self.manager.current = "Home"
        self.manager.TransitionBase = "FadeTransition"


class HomeScreen(Screen):
    pass


class ResourceScreen(Screen):
    pass


class QuoteScreen(Screen):
    pass


class Tab(Screen):
    pass


class TestApp(App):
    def build(self):
        self.fl = FloatLayout()
        self.size = Window.size
        return ScreenManagement()

    def showTab(self):
        return Tab()

    #Window.fullscreen = True


TestApp().run()