"""
This module defines the App class and provides functions for reading macro files.
"""

import os

class App:
    """
    Represents a host-side application with a set of macro sequences.
    """
    def __init__(self, appdata, filename, folder=''):
        self.name = appdata['name']
        self.macros = appdata['macros']
        self.filename = filename
        self.folder = folder

    def switch(self, macropad, group):
        """
        Activate application settings; update OLED labels and LED colors.
        """
        group[13].text = self.name   # Application name
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()

def read_macro_files(folder):
    """
    Read all macro key setups from .py files in the given folder and its subfolders.
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
        elif os.stat(folder + '/' + filename)[0] & 0x4000:  # Check if it's a directory
            subfolder = folder + '/' + filename
            subapps = read_macro_files(subfolder)
            if subapps:
                apps.append((filename, subapps))
    return apps