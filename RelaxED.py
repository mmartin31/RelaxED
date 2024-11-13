from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, TransitionBase
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import random
import re


class ScreenManagement(ScreenManager):
    pass


class LoadingScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(self.popup, 3)

    def change_screen(self, press):
        self.pop.dismiss()
        self.manager.current = "Home"
        self.manager.TransitionBase = "FadeTransition"

    def popup(self, dt):
        layout = GridLayout(cols=1, padding=10)

        # Load text from a file
        try:
            with open("consent.txt", "r") as file:
                popup_text = file.read()
        except FileNotFoundError:
            popup_text = "Consent file not found. Please contact support."

        popupLabel = Label(text=popup_text)
        closeButton = Button(text="I agree", size_hint=(None, None), size=(200, 200))

        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)

        # Instantiate the modal popup and display
        self.pop = Popup(title='Consent to use app', content=layout, size_hint=(None, None), size=(2000, 1800))
        self.pop.open()

        # Attach close button press with popup.dismiss action
        closeButton.bind(on_press=self.change_screen)


class HomeScreen(Screen):
    pass


class ResourceScreen(Screen):
    pass


class ScreeningToolsScreen(Screen):
    pass


class AnxietyEDScreen(Screen):
    pass


class LocalResourcesScreen(Screen):
    pass


class QuoteScreen(Screen):
    quotes = []  # This will store the quotes list for reuse

    def on_enter(self):
        if not self.quotes:  # Only load quotes if they haven't been loaded already
            self.quotes = self.load_quotes()  # Load quotes on screen enter if necessary
        self.display_random_quote()  # Display a random quote

    def load_quotes(self):
        quotes = []
        try:
            with open("quotes.txt", "r", encoding="utf-8") as file:
                content = file.read()  # Read the entire file content at once

                # Manually process content to extract quotes based on numbers at the start
                current_quote = ""
                for line in content.splitlines():
                    # Check if the line starts with a number followed by a period (e.g., "1.")
                    if line and line[0].isdigit() and '.' in line:
                        if current_quote:  # If we already have a current quote, save it
                            quotes.append(current_quote.strip())  # Add the previous quote
                        current_quote = line  # Start a new quote
                    else:
                        # Append the line to the current quote if it's part of the same quote
                        current_quote += " " + line

                # Append the last quote after the loop finishes
                if current_quote:
                    quotes.append(current_quote.strip())
        except FileNotFoundError:
            return ["Quotes file not found. Please contact support."]

        return quotes

    def display_random_quote(self):
        if not self.quotes:
            self.ids.quote_label.text = "No quotes available."
        else:
            random_quote = random.choice(self.quotes)
            self.ids.quote_label.text = random_quote


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
