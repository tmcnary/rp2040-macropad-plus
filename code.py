"""
Adafruit MacroPad Hotkeys: Main Program

This is the main entry point for the Adafruit MacroPad Hotkeys application.
It initializes the MacroPad, sets up handlers for various functionalities,
and runs the main event loop.

Features:
- Dynamic loading of macro files from the /macros folder
- Menu navigation for selecting macro sets
- Favorites functionality for quick access to preferred macros
- Tap-dance feature for extended key press actions

Author: YourName
Date: YYYY-MM-DD
License: MIT

Dependencies:
- adafruit_macropad
- modules.macropad_handler
- modules.menu_handler
- modules.favorites_handler
- modules.tap_dance
- modules.utils
"""

import time
from adafruit_macropad import MacroPad
from modules.macropad_handler import MacroPadHandler
from modules.menu_handler import MenuHandler
from modules.favorites_handler import FavoritesHandler
from modules.tap_dance import TapDance
from modules.utils import MACRO_FOLDER

# Initialize the MacroPad
macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Initialize handlers
handler = MacroPadHandler(macropad)
menu = MenuHandler(macropad, handler)
favorites = FavoritesHandler()
tap_dance = TapDance()

# Load macro files and set initial app
apps = handler.read_macro_files()

if not apps:
    handler.show_error('NO MACRO FILES FOUND')
    while True:
        pass

current_app = apps[0] if isinstance(apps[0], handler.App) else apps[0][1][0]
handler.switch_app(current_app)

# Main event loop
last_encoder_position = macropad.encoder
setting_favorite = False

while True:
    # Handle encoder button press
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        selected_item = menu.navigate_menu(apps)
        if selected_item:
            if isinstance(selected_item, handler.App):
                current_app = selected_item
            elif isinstance(selected_item, tuple):  # It's a folder
                current_app = selected_item[1][0]  # Select first app in the folder
            handler.switch_app(current_app)
        last_encoder_position = macropad.encoder
    
    # Handle encoder rotation
    current_encoder_position = macropad.encoder
    if current_app.folder != MACRO_FOLDER and current_encoder_position != last_encoder_position:
        current_app = handler.handle_encoder_rotation(current_app, current_encoder_position - last_encoder_position)
        last_encoder_position = current_encoder_position

    # Handle key events
    event = macropad.keys.events.get()
    if event:
        key_number = event.key_number
        pressed = event.pressed

        if key_number < len(current_app.macros):
            if current_app.name == 'Favorites':
                favorites.handle_favorites(handler, current_app, key_number, pressed, setting_favorite)
            elif setting_favorite:
                favorites.set_favorite(key_number, current_app)
                setting_favorite = False
                handler.show_message('Favorite Set', 1)
                handler.switch_app(current_app)
            else:
                tap_dance.handle_tap_dance(handler, current_app, key_number, pressed)

            handler.update_pixel(key_number, pressed, current_app)

    # Check for long press
    tap_dance.check_long_press(handler, current_app)

    # Small delay to prevent excessive CPU usage
    time.sleep(0.01)