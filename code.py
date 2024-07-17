"""
SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
SPDX-License-Identifier: MIT

Main script for the Adafruit MacroPad Hotkeys project.
This script initializes the MacroPad, loads apps, and runs the main loop.
"""

import time
from adafruit_macropad import MacroPad
from modules.app import App, read_macro_files
from modules.display import setup_display, show_group
from modules.menu import navigate_menu
from modules.macro_handler import handle_key_event

# Configurables
MACRO_FOLDER = '/macros'

# Initialize MacroPad
macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Set up display
group = setup_display(macropad)
show_group(macropad, group)

# Load macro files
apps = read_macro_files(MACRO_FOLDER)

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

current_app = apps[0] if isinstance(apps[0], App) else apps[0][1][0]
current_app.switch(macropad, group)

# Initialize encoder position
last_encoder_position = macropad.encoder

# Main loop
while True:
    # Check if encoder button is pressed to open menu
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        selected_item = navigate_menu(macropad, apps)
        if selected_item:
            if isinstance(selected_item, App):
                current_app = selected_item
            elif isinstance(selected_item, tuple):  # It's a folder
                current_app = selected_item[1][0]  # Select first app in the folder
            current_app.switch(macropad, group)
        show_group(macropad, group)
        last_encoder_position = macropad.encoder
    
    # Handle encoder rotation for selecting macros within a subfolder
    current_encoder_position = macropad.encoder
    if current_app.folder != MACRO_FOLDER and current_encoder_position != last_encoder_position:
        current_folder_name = current_app.folder.split('/')[-1]  # Get the last part of the folder path
        current_folder = [app for app in apps if isinstance(app, tuple) and app[0] == current_folder_name][0][1]
        current_index = current_folder.index(current_app)
        encoder_change = current_encoder_position - last_encoder_position
        new_index = (current_index + encoder_change) % len(current_folder)
        current_app = current_folder[new_index]
        current_app.switch(macropad, group)
        last_encoder_position = current_encoder_position

    # Handle key events
    event = macropad.keys.events.get()
    if event:
        handle_key_event(macropad, current_app, event)

    # Small delay to prevent excessive CPU usage
    time.sleep(0.01)