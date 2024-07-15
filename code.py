"""
SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
SPDX-License-Identifier: MIT

A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.

This version includes a new app selection mechanism:
- Turning the encoder activates a menu with a list of available macros.
- Turning the encoder scrolls through the list and highlights macros.
- Pressing the encoder button selects the highlighted macro.
- If no selection is made within 3 seconds, it returns to the current macro.
"""

import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad


# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'
MENU_ITEMS = 5  # Number of menu items to display (odd number)


# CLASSES AND FUNCTIONS ----------------

class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. """
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']

    def switch(self):
        """ Activate application settings; update OLED labels and LED
            colors. """
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


def read_macro_files():
    """ Read all the macro key setups from .py files in MACRO_FOLDER """
    apps = []
    files = os.listdir(MACRO_FOLDER)
    files.sort()
    for filename in files:
        if filename.endswith('.py') and not filename.startswith('._'):
            try:
                module = __import__(MACRO_FOLDER + '/' + filename[:-3])
                apps.append(App(module.app))
            except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                    IndexError, TypeError) as err:
                print("ERROR in", filename)
                import traceback
                traceback.print_exception(err, err, err.__traceback__)
    return apps


def show_menu(apps, current_app):
    """ Display the app selection menu """
    menu_group = displayio.Group()

    # Calculate the range of items to display
    total_items = len(apps)
    half_display = MENU_ITEMS // 2
    start_index = max(0, min(current_app - half_display, total_items - MENU_ITEMS))
    end_index = min(start_index + MENU_ITEMS, total_items)

    # Background for selected item
    selected_bg = Rect(0, (MENU_ITEMS // 2) * 12, macropad.display.width, 12, fill=0xFFFFFF)
    menu_group.append(selected_bg)

    # Create labels for the visible items
    for i in range(start_index, end_index):
        is_selected = (i == current_app)
        text = apps[i].name
        y_position = ((i - start_index) * 12) + 6  # Center text vertically in each row
        menu_label = label.Label(
            terminalio.FONT,
            text=text,
            color=0x000000 if is_selected else 0xFFFFFF,
            anchored_position=(macropad.display.width - 1, y_position),
            anchor_point=(1.0, 0.5)  # Right-align the text
        )
        menu_group.append(menu_label)

    macropad.display.root_group = menu_group
    macropad.display.refresh()


# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                             anchor_point=(x / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         anchored_position=(macropad.display.width//2, -1),
                         anchor_point=(0.5, 0.0)))
macropad.display.root_group = group

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = read_macro_files()

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

last_position = None
app_index = 0
apps[app_index].switch()


# MAIN LOOP ----------------------------

while True:
    # Read encoder position.
    position = macropad.encoder

    if position != last_position:
        # Encoder turned, show menu
        app_index = position % len(apps)
        show_menu(apps, app_index)
        menu_active = True
        menu_timeout = time.monotonic() + 3  # 3 second timeout

        while menu_active:
            macropad.encoder_switch_debounced.update()
            current_position = macropad.encoder
            if current_position != position:
                # Scroll through menu
                position = current_position
                app_index = position % len(apps)
                show_menu(apps, app_index)
                menu_timeout = time.monotonic() + 3  # Reset timeout

            if macropad.encoder_switch_debounced.pressed:
                # Selection made
                menu_active = False
                apps[app_index].switch()
                macropad.display.root_group = group
                macropad.display.refresh()

            if time.monotonic() > menu_timeout:
                # Timeout, return to current app
                menu_active = False
                macropad.display.root_group = group
                macropad.display.refresh()

        last_position = position

    # Handle key events
    event = macropad.keys.events.get()
    if event:
        key_number = event.key_number
        pressed = event.pressed

        if key_number < len(apps[app_index].macros):
            sequence = apps[app_index].macros[key_number][2]
            if pressed:
                if key_number < 12: # No pixel for encoder button
                    macropad.pixels[key_number] = 0xFFFFFF
                    macropad.pixels.show()
                for item in sequence:
                    if isinstance(item, int):
                        if item >= 0:
                            macropad.keyboard.press(item)
                        else:
                            macropad.keyboard.release(-item)
                    elif isinstance(item, float):
                        time.sleep(item)
                    elif isinstance(item, str):
                        macropad.keyboard_layout.write(item)
                    elif isinstance(item, list):
                        for code in item:
                            if isinstance(code, int):
                                macropad.consumer_control.release()
                                macropad.consumer_control.press(code)
                            if isinstance(code, float):
                                time.sleep(code)
                    elif isinstance(item, dict):
                        if 'buttons' in item:
                            if item['buttons'] >= 0:
                                macropad.mouse.press(item['buttons'])
                            else:
                                macropad.mouse.release(-item['buttons'])
                        macropad.mouse.move(item['x'] if 'x' in item else 0,
                                            item['y'] if 'y' in item else 0,
                                            item['wheel'] if 'wheel' in item else 0)
                        if 'tone' in item:
                            if item['tone'] > 0:
                                macropad.stop_tone()
                                macropad.start_tone(item['tone'])
                            else:
                                macropad.stop_tone()
                        elif 'play' in item:
                            macropad.play_file(item['play'])
            else:
                # Release any still-pressed keys, consumer codes, mouse buttons
                for item in sequence:
                    if isinstance(item, int):
                        if item >= 0:
                            macropad.keyboard.release(item)
                    elif isinstance(item, dict):
                        if 'buttons' in item:
                            if item['buttons'] >= 0:
                                macropad.mouse.release(item['buttons'])
                        elif 'tone' in item:
                            macropad.stop_tone()
                macropad.consumer_control.release()
                if key_number < 12: # No pixel for encoder button
                    macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
                    macropad.pixels.show()