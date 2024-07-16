# SPDX-FileCopyrightText: 2021 Your Name for Custom Macropad Configuration
# SPDX-License-Identifier: MIT

from adafruit_hid.keycode import Keycode

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Tabs',       # Application name
    'macros' : [           # List of button macros...
        # COLOR     LABEL      KEY SEQUENCE
        # 1st row ----------
        (0xFF5733, 'Tab 1', [Keycode.COMMAND, '1']),  # Random color
        (0x33FF57, 'Tab 2', [Keycode.COMMAND, '2']),  # Random color
        (0x5733FF, 'Tab 3', [Keycode.COMMAND, '3']),  # Random color
        # 2nd row ----------
        (0xFFFF33, 'Tab 4', [Keycode.COMMAND, '4']),  # Random color
        (0x33FFFF, 'Tab 5', [Keycode.COMMAND, '5']),  # Random color
        (0xFF33FF, 'Tab 6', [Keycode.COMMAND, '6']),  # Random color
        # 3rd row ----------
        (0xFF3333, 'Tab 7', [Keycode.COMMAND, '7']),  # Random color
        (0x33FF33, 'Tab 8', [Keycode.COMMAND, '8']),  # Random color
        (0x3333FF, 'Tab 9', [Keycode.COMMAND, '9']),  # Random color
        # 4th row ----------
        (0xAAFF33, 'Back', [Keycode.COMMAND, '[']),   # Same color for back
        (0xFFA500, 'Refresh', [Keycode.COMMAND, 'R']), # Random color for refresh
        (0xAAFF33, 'Forward', [Keycode.COMMAND, ']']) # Same color for forward
    ]
}
