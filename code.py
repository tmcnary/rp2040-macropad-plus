"""
SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
SPDX-License-Identifier: MIT

A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), with support for subfolder grouping.
This version includes Favorites functionality and Tap-Dance feature for extended button functionality.
"""

import os
import time
import json
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'
MENU_ITEMS = 5  # Number of menu items to display (odd number)
FAVORITES_FILE = '/favorites.json'
TAP_DANCE_TIMEOUT = 0.3  # Time window for double tap (in seconds)
HOLD_TIMEOUT = 0.5  # Time threshold for long press (in seconds)

# CLASSES AND FUNCTIONS ----------------

class App:
    def __init__(self, appdata, filename, folder=''):
        self.name = appdata['name']
        self.macros = appdata['macros']
        self.filename = filename
        self.folder = folder

    def switch(self):
        group[13].text = self.name
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

def read_macro_files(folder=MACRO_FOLDER):
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
            subapps = read_macro_files(subfolder)
            if subapps:
                apps.append((filename, subapps))
    return apps

def show_menu(items, current_item, inverse=False):
    menu_group = displayio.Group()
    total_items = len(items)
    half_display = MENU_ITEMS // 2
    start_index = max(0, min(current_item - half_display, total_items - MENU_ITEMS))
    end_index = min(start_index + MENU_ITEMS, total_items)

    for i in range(start_index, end_index):
        is_selected = (i == current_item)
        item = items[i]
        text = item[0] if isinstance(item, tuple) else item.name
        if isinstance(item, tuple):
            text = f"[{text}]"
        y_position = ((i - start_index) * 12) + 6
        
        if is_selected:
            selected_bg = Rect(0, (i - start_index) * 12, macropad.display.width, 12, fill=0x000000 if inverse else 0xFFFFFF)
            menu_group.append(selected_bg)
        
        menu_label = label.Label(
            terminalio.FONT,
            text=text,
            color=0xFFFFFF if (inverse and is_selected) else (0x000000 if is_selected else 0xFFFFFF),
            anchored_position=(macropad.display.width - 1, y_position),
            anchor_point=(1.0, 0.5)
        )
        menu_group.append(menu_label)

    macropad.display.root_group = menu_group
    macropad.display.refresh()

def flash_selected(items, current_item):
    for _ in range(2):
        show_menu(items, current_item, inverse=True)
        time.sleep(0.05)
        show_menu(items, current_item, inverse=False)
        time.sleep(0.05)

def navigate_menu(items):
    current_item = 0
    show_menu(items, current_item)
    menu_timeout = time.monotonic() + 3
    last_encoder_position = macropad.encoder

    while True:
        macropad.encoder_switch_debounced.update()
        current_encoder_position = macropad.encoder
        
        if current_encoder_position != last_encoder_position:
            current_item = (current_item + current_encoder_position - last_encoder_position) % len(items)
            show_menu(items, current_item)
            menu_timeout = time.monotonic() + 3
            last_encoder_position = current_encoder_position

        if macropad.encoder_switch_debounced.pressed:
            flash_selected(items, current_item)
            return items[current_item]

        if time.monotonic() > menu_timeout:
            return None

        time.sleep(0.01)

def load_favorites():
    try:
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f)

def set_favorite(key, app):
    favorites = load_favorites()
    favorites[str(key)] = {'name': app.name, 'filename': app.filename, 'folder': app.folder}
    save_favorites(favorites)

def get_favorite(key):
    favorites = load_favorites()
    if str(key) in favorites:
        fav = favorites[str(key)]
        for app in apps:
            if isinstance(app, App) and app.filename == fav['filename'] and app.folder == fav['folder']:
                return app
    return None

def execute_macro(sequence):
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

def handle_tap_dance(key_number, pressed):
    global last_press_time, tap_count, is_long_press

    current_time = time.monotonic()
    
    if pressed:
        if current_time - last_press_time <= TAP_DANCE_TIMEOUT:
            tap_count += 1
        else:
            tap_count = 1
        last_press_time = current_time
        is_long_press = False
    else:
        if current_time - last_press_time >= HOLD_TIMEOUT:
            if is_long_press:
                # Tap and Hold (Action 4)
                execute_macro(current_app.macros[key_number][2][3])
            else:
                # Hold (Action 3)
                execute_macro(current_app.macros[key_number][2][2])
        elif tap_count == 1:
            # Single Tap (Action 1)
            execute_macro(current_app.macros[key_number][2][0])
        elif tap_count == 2:
            # Double Tap (Action 2)
            execute_macro(current_app.macros[key_number][2][1])
        
        tap_count = 0
        is_long_press = False

# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

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

apps = read_macro_files()

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

current_app = apps[0] if isinstance(apps[0], App) else apps[0][1][0]
current_app.switch()

# MAIN LOOP ----------------------------

last_encoder_position = macropad.encoder
setting_favorite = False
last_press_time = 0
tap_count = 0
is_long_press = False

while True:
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        selected_item = navigate_menu(apps)
        if selected_item:
            if isinstance(selected_item, App):
                current_app = selected_item
                current_app.switch()
            elif isinstance(selected_item, tuple):
                current_app = selected_item[1][0]
                current_app.switch()
        macropad.display.root_group = group
        macropad.display.refresh()
        last_encoder_position = macropad.encoder
    
    current_encoder_position = macropad.encoder
    if current_app.folder != MACRO_FOLDER and current_encoder_position != last_encoder_position:
        current_folder_name = current_app.folder.split('/')[-1]
        current_folder = [app for app in apps if isinstance(app, tuple) and app[0] == current_folder_name][0][1]
        current_index = current_folder.index(current_app)
        encoder_change = current_encoder_position - last_encoder_position
        new_index = (current_index + encoder_change) % len(current_folder)
        current_app = current_folder[new_index]
        current_app.switch()
        last_encoder_position = current_encoder_position

    event = macropad.keys.events.get()
    if event:
        key_number = event.key_number
        pressed = event.pressed

        if key_number < len(current_app.macros):
            if current_app.name == 'Favorites':
                if pressed:
                    sequence = current_app.macros[key_number][2]
                    if sequence[0] == 'SET_FAVORITE':
                        setting_favorite = True
                        group[13].text = 'Set Favorite'
                        macropad.display.refresh()
                    elif sequence[0] == 'BACK_TO_MAIN':
                        current_app = apps[0] if isinstance(apps[0], App) else apps[0][1][0]
                        current_app.switch()
                    elif sequence[0].startswith('FAVORITE_'):
                        fav_num = int(sequence[0].split('_')[1])
                        fav_app = get_favorite(fav_num - 1)
                        if fav_app:
                            current_app = fav_app
                            current_app.switch()
            elif setting_favorite:
                if pressed:
                    set_favorite(key_number, current_app)
                    setting_favorite = False
                    group[13].text = 'Favorite Set'
                    macropad.display.refresh()
                    time.sleep(1)
                    current_app.switch()
            else:
                handle_tap_dance(key_number, pressed)

            if pressed and key_number < 12:
                macropad.pixels[key_number] = 0xFFFFFF
                macropad.pixels.show()
            elif not pressed and key_number < 12:
                macropad.pixels[key_number] = current_app.macros[key_number][0]
                macropad.pixels.show()

    # Check for long press
    if time.monotonic() - last_press_time >= HOLD_TIMEOUT and not is_long_press:
        is_long_press = True
        # This will trigger the Hold action when the key is released