# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

# CONFIGURABLES ------------------------
MACRO_FOLDER = '/macros'
SELECTION_TIMEOUT = 3  # seconds

# CLASSES AND FUNCTIONS ----------------
class App:
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']

    def switch(self):
        group[13].text = self.name
        group[13].color = 0xFFFFFF
        if self.name:
            rect.fill = 0x000000
        for i in range(12):
            if i < len(self.macros):
                macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()

def load_apps():
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

def show_app_selection(apps, selected_index):
    # Clear the display
    for i in range(14):
        group[i].text = ''
    
    rect.fill = 0x000000  # Set background to black
    
    # Calculate which apps to show
    start = (selected_index // 4) * 4
    end = min(len(apps), start + 4)
    
    # Show apps
    for i, app in enumerate(apps[start:end], start=start):
        group[i - start].text = app.name
        group[i - start].anchored_position = (5, (i - start + 1) * 8)
        group[i - start].scale = 1
        if i == selected_index:
            group[i - start].color = 0xFFFF00  # Yellow for selected
        else:
            group[i - start].color = 0xFFFFFF  # White for unselected
    
    # Show selection indicator
    group[13].text = f"{selected_index + 1}/{len(apps)}"
    group[13].anchored_position = (macropad.display.width - 5, macropad.display.height - 5)
    group[13].anchor_point = (1.0, 1.0)
    group[13].scale = 1
    group[13].color = 0xFFFFFF
    
    macropad.display.refresh()

def select_app(apps, current_app_index):
    selected_index = current_app_index
    show_app_selection(apps, selected_index)
    last_encoder_position = macropad.encoder
    selection_start_time = time.monotonic()

    while True:
        current_position = macropad.encoder
        if current_position != last_encoder_position:
            selected_index = (selected_index + current_position - last_encoder_position) % len(apps)
            show_app_selection(apps, selected_index)
            last_encoder_position = current_position
            selection_start_time = time.monotonic()

        macropad.encoder_switch_debounced.update()
        if macropad.encoder_switch_debounced.pressed:
            return selected_index

        if time.monotonic() - selection_start_time > SELECTION_TIMEOUT:
            return current_app_index

        time.sleep(0.01)

# INITIALIZATION -----------------------
macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(14):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=(0, 0),
                             anchor_point=(0, 0)))
rect = Rect(0, 0, macropad.display.width, macropad.display.height, fill=0x000000)
group.insert(0, rect)  # Add the rectangle as the background
macropad.display.root_group = group

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = load_apps()

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

last_position = macropad.encoder
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()

# MAIN LOOP ----------------------------
while True:
    position = macropad.encoder
    if position != last_position:
        app_index = select_app(apps, app_index)
        apps[app_index].switch()
        last_position = position
        continue

    # Handle key presses
    event = macropad.keys.events.get()
    if event:
        key_number = event.key_number
        pressed = event.pressed

        if key_number < len(apps[app_index].macros):
            sequence = apps[app_index].macros[key_number][2]
            if pressed:
                if key_number < 12:
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
                # Release actions
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
                if key_number < 12:
                    macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
                    macropad.pixels.show()

    time.sleep(0.01)  # Small delay to keep things responsive but not too busy