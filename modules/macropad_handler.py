"""
MacroPad Handler Module

This module provides a handler class for the Adafruit MacroPad, managing
the display, pixels, and macro execution.

Classes:
- App: Represents a macro application with its associated data.
- MacroPadHandler: Handles MacroPad operations and macro execution.

Author: YourName
Date: YYYY-MM-DD
License: MIT
"""

import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from modules.utils import MACRO_FOLDER

class App:
    """
    Represents a macro application.

    Attributes:
        name (str): The name of the application.
        macros (list): List of macros associated with the application.
        filename (str): The filename of the macro file.
        folder (str): The folder containing the macro file.
    """
    def __init__(self, appdata, filename, folder=''):
        self.name = appdata['name']
        self.macros = appdata['macros']
        self.filename = filename
        self.folder = folder

class MacroPadHandler:
    """
    Handles MacroPad operations and macro execution.

    Methods:
        read_macro_files: Reads macro files from the specified folder.
        switch_app: Switches to a new application, updating display and pixels.
        handle_encoder_rotation: Handles encoder rotation for app switching.
        update_pixel: Updates a single pixel on the MacroPad.
        show_error: Displays an error message on the MacroPad.
        show_message: Displays a temporary message on the MacroPad.
        execute_sequence: Executes a macro sequence.
    """

    def __init__(self, macropad):
        """
        Initializes the MacroPadHandler.

        Args:
            macropad: The MacroPad object to handle.
        """
        self.macropad = macropad
        self.group = self._setup_display_group()
        self.macropad.display.root_group = self.group

    def _setup_display_group(self):
        """
        Sets up the display group for the MacroPad's OLED screen.

        Returns:
            displayio.Group: The configured display group.
        """
        group = displayio.Group()
        for key_index in range(12):
            x = key_index % 3
            y = key_index // 3
            group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                                     anchored_position=((self.macropad.display.width - 1) * x / 2,
                                                        self.macropad.display.height - 1 -
                                                        (3 - y) * 12),
                                     anchor_point=(x / 2, 1.0)))
        group.append(Rect(0, 0, self.macropad.display.width, 12, fill=0xFFFFFF))
        group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                                 anchored_position=(self.macropad.display.width//2, -1),
                                 anchor_point=(0.5, 0.0)))
        return group

    def read_macro_files(self, folder=MACRO_FOLDER):
        """
        Reads macro files from the specified folder.

        Args:
            folder (str): The folder to read macro files from.

        Returns:
            list: A list of App objects and tuples representing folders.
        """
        apps = []
        files = os.listdir(folder)
        files.sort()
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('._'):
                try:
                    module = __import__(folder + '/' + filename[:-3])
                    apps.append(App(module.app, filename, folder=folder))
                except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                        IndexError, TypeError) as err:
                    print("ERROR in", filename)
                    import traceback
                    traceback.print_exception(err, err, err.__traceback__)
            elif os.stat(folder + '/' + filename)[0] & 0x4000:
                subfolder = folder + '/' + filename
                subapps = self.read_macro_files(subfolder)
                if subapps:
                    apps.append((filename, subapps))
        return apps

    def switch_app(self, app):
        """
        Switches to a new application, updating display and pixels.

        Args:
            app (App): The application to switch to.
        """
        self.group[13].text = app.name
        for i in range(12):
            if i < len(app.macros):
                self.macropad.pixels[i] = app.macros[i][0]
                self.group[i].text = app.macros[i][1]
            else:
                self.macropad.pixels[i] = 0
                self.group[i].text = ''
        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()
        self.macropad.pixels.show()
        self.macropad.display.refresh()

    def handle_encoder_rotation(self, current_app, encoder_change):
        """
        Handles encoder rotation for app switching within a folder.

        Args:
            current_app (App): The current application.
            encoder_change (int): The change in encoder position.

        Returns:
            App: The new application after rotation.
        """
        current_folder_name = current_app.folder.split('/')[-1]
        current_folder = [app for app in self.read_macro_files() if isinstance(app, tuple) and app[0] == current_folder_name][0][1]
        current_index = current_folder.index(current_app)
        new_index = (current_index + encoder_change) % len(current_folder)
        new_app = current_folder[new_index]
        self.switch_app(new_app)
        return new_app

    def update_pixel(self, key_number, pressed, current_app):
        """
        Updates a single pixel on the MacroPad.

        Args:
            key_number (int): The key number to update.
            pressed (bool): Whether the key is pressed or released.
            current_app (App): The current application.
        """
        if pressed and key_number < 12:
            self.macropad.pixels[key_number] = 0xFFFFFF
        elif not pressed and key_number < 12:
            self.macropad.pixels[key_number] = current_app.macros[key_number][0]
        self.macropad.pixels.show()

    def show_error(self, message):
        """
        Displays an error message on the MacroPad.

        Args:
            message (str): The error message to display.
        """
        self.group[13].text = message
        self.macropad.display.refresh()

    def show_message(self, message, duration):
        """
        Displays a temporary message on the MacroPad.

        Args:
            message (str): The message to display.
            duration (float): The duration to display the message in seconds.
        """
        self.group[13].text = message
        self.macropad.display.refresh()
        time.sleep(duration)

    def execute_sequence(self, sequence):
        """
        Executes a macro sequence.

        Args:
            sequence (list): The macro sequence to execute.
        """
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    self.macropad.keyboard.press(item)
                else:
                    self.macropad.keyboard.release(-item)
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, str):
                self.macropad.keyboard_layout.write(item)
            elif isinstance(item, list):
                for code in item:
                    if isinstance(code, int):
                        self.macropad.consumer_control.release()
                        self.macropad.consumer_control.press(code)
                    if isinstance(code, float):
                        time.sleep(code)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        self.macropad.mouse.press(item['buttons'])
                    else:
                        self.macropad.mouse.release(-item['buttons'])
                self.macropad.mouse.move(item['x'] if 'x' in item else 0,
                                         item['y'] if 'y' in item else 0,
                                         item['wheel'] if 'wheel' in item else 0)
                if 'tone' in item:
                    if item['tone'] > 0:
                        self.macropad.stop_tone()
                        self.macropad.start_tone(item['tone'])
                    else:
                        self.macropad.stop_tone()
                elif 'play' in item:
                    self.macropad.play_file(item['play'])