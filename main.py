from kivy.clock import Clock
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import random
from kivy.lang import Builder
from kivy.resources import resource_add_path
import os
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout


class ScreenManagement(ScreenManager):
    """Main screen manager class that handles all screen transitions."""
    pass


class LoadingScreen(Screen):
    """Class for initial loading screen that displays the consent popup."""
    def on_enter(self):
        """Schedules the consent popup to appear 3 seconds after the app is opened."""
        Clock.schedule_once(self.popup, 3)

    def change_screen(self, press):
        """Handles transition to home screen once consent is given.

        Args:
            press: button press event instance
        """
        self.pop.dismiss()
        self.manager.current = "Home"
        self.manager.TransitionBase = "FadeTransition"

    def popup(self, dt):
        """Creates and displays the consent popup.

        Args:
            dt: Delta Time (required by Clock)
        """
        # Main layout for the popup
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create scroll view for the text
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, 0.9))

        # Content layout inside scroll view
        content_layout = BoxLayout(orientation='vertical', size_hint_y=None, size_hint_x=1, padding=10)

        # Bind the height of the content layout to its minimum height
        content_layout.bind(minimum_height=content_layout.setter('height'))

        # Load text from file
        try:
            with open("text/consent.txt", "r") as file:
                # Read content and split into paragraphs (double newlines)
                paragraphs = file.read().split('\n\n')
                # Clean up each paragraph (remove single line breaks)
                cleaned_paragraphs = [' '.join(p.split()) for p in paragraphs]
                # Join paragraphs with double newlines
                popup_text = '\n\n'.join(cleaned_paragraphs)
        except FileNotFoundError:
            popup_text = "Consent file not found."

        # Create label with text wrapping
        popup_label = Label(text=popup_text,
                            size_hint_y=None,
                            size_hint_x=1,
                            text_size=(None, None),
                            halign='left',
                            valign='top',
                            padding=(10, 10),
                            markup=True)

        # Bind width to parent to ensure proper text wrapping
        popup_label.bind(
            width=lambda *x: setattr(popup_label, 'text_size', (popup_label.width, None)),
            texture_size=lambda *x: setattr(popup_label, 'height', popup_label.texture_size[1]))

        # Add label to content layout
        content_layout.add_widget(popup_label)

        # Add content layout to scroll view
        scroll.add_widget(content_layout)

        # Create accept button
        close_button = Button(text="I agree",
                              size_hint=(None, None),
                              pos_hint={'center_x': 0.5},
                              size=(200, 200))

        # Button container for proper spacing
        button_container = BoxLayout(size_hint_y=0.1, padding=(0, 10))
        button_container.add_widget(close_button)

        # Add scroll view and button to main layout
        layout.add_widget(scroll)
        layout.add_widget(button_container)

        # Instantiate the popup and display
        self.pop = Popup(title='Consent to use app',
                         title_size='24sp',
                         content=layout,
                         size_hint=(0.8, 0.9),
                         auto_dismiss=False)
        self.pop.open()

        # Bind button to close action
        close_button.bind(on_press=self.change_screen)


class HomeScreen(Screen):
    """Class for Home Screen

    This screen serves as the main navigation center for the app,
    providing access to various features including:
    - Resource Screen (takes you to other features)
    - Daily Quote Screen

    The screen layout and styling are defined in the home_screen.kv file.
    """
    pass


class ResourceScreen(Screen):
    """Class for Resource Screen"""
    pass


class ScreeningToolsScreen(Screen):
    """Class for Screening Tools Screen"""
    pass


class AnxietyEDScreen(Screen):
    """Class for Anxiety Education Screen"""
    pass


class LocalResourcesScreen(Screen):
    """Class for Local Resources Screen"""
    pass


class QuoteScreen(Screen):
    """Class for Quote Screen management."""
    quotes = []  # This will store the quotes list for reuse

    def on_enter(self):
        """Loads quotes if necessary and displays a random one when screen is entered."""
        if not self.quotes:  # Only load quotes if they haven't been loaded already
            self.quotes = self.load_quotes()  # Load quotes on screen enter if necessary
        self.display_random_quote()  # Display a random quote

    def load_quotes(self):
        """Loads quotes from the quotes.txt file.

        Returns:
            list: list of quotes, or error message if file not found"""
        quotes = []
        try:
            with open("text/quotes.txt", "r", encoding="utf-8") as file:
                content = file.read()  # Read the entire file content at once

                # Process content to extract quotes based on numbers at the start
                current_quote = ""
                for line in content.splitlines():
                    # Check if the line starts with a number followed by a period (ex. "1.")
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
            return ["Quotes file not found."]

        return quotes

    def display_random_quote(self):
        """Selects and displays a random quote from the loaded quotes."""
        if not self.quotes:
            self.ids.quote_label.text = "No quotes available."
        else:
            random_quote = random.choice(self.quotes)
            self.ids.quote_label.text = random_quote


def load_kv_files():
    """Loads kivy files from the kv directory.

    The function adds the kv directory to the resource path and loads main.kv,
    which then includes all other .kv files through #:include directives:
    - styles.kv (common styles)
    - All screen-specific .kv files from the screens subdirectory
    """
    try:
        # Add the kv directory to resource path
        resource_add_path(os.path.join(os.getcwd(), 'kv'))

        # Load main.kv which includes all other kv files
        Builder.load_file('kv/main.kv')
    except Exception as e:
        print(f"Error loading KV files: {e}")


class TestApp(App):
    """Main application class for the BreathWell app."""
    def build(self):
        """Loads kivy files and returns the screen manager"""
        # Load all KV files
        load_kv_files()

        return ScreenManagement()


# Run the app
TestApp().run()
