# SPDX-FileCopyrightText: 2021 Your Name for Custom Macropad Configuration
# SPDX-License-Identifier: MIT

from adafruit_hid.keycode import Keycode

app = {                      # REQUIRED dict, must be named 'app'
    'name' : 'Nav',          # Application name
    'macros' : [             # List of button macros...
        # COLOR     LABEL        KEY SEQUENCE
        # 1st row ----------
        (0x00FF00, 'Tab Up', [Keycode.OPTION, Keycode.COMMAND, Keycode.UP_ARROW]),    # 1: Switch between tabs up
        (0xFFFF00, 'Back [', [Keycode.COMMAND, '[']),                                 # 2: Go back on tab history
        (0xFF00FF, 'Fwd ]', [Keycode.COMMAND, ']']),                                  # 3: Go forward on tab history
        # 2nd row ----------
        (0x00FF00, 'Tab Down', [Keycode.OPTION, Keycode.COMMAND, Keycode.DOWN_ARROW]),# 4: Switch between tabs down
        (0xFFFF00, 'Back <', [Keycode.COMMAND, Keycode.LEFT_ARROW]),                  # 5: Go back on tab history
        (0xFF00FF, 'Fwd >', [Keycode.COMMAND, Keycode.RIGHT_ARROW]),                  # 6: Go forward on tab history
        # 3rd row ----------
        (0x0000FF, 'Space L', [Keycode.OPTION, Keycode.COMMAND, Keycode.LEFT_ARROW]), # 7: Switch between spaces left
        (0x0000FF, 'Space R', [Keycode.OPTION, Keycode.COMMAND, Keycode.RIGHT_ARROW]),# 8: Switch between spaces right
        (0xFF0000, 'Tab <->', [Keycode.CONTROL, Keycode.TAB]),                        # 9: Toggle between recent tabs
        # 4th row ----------
        (0x000000, 'Close', [Keycode.COMMAND, 'W']),                                  # 10: Close tab
        (0x000000, '', []),                                                           # 11: Empty
        (0x000000, '', [])                                                            # 12: Empty
    ]
}
