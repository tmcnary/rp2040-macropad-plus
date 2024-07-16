# SPDX-FileCopyrightText: 2021 Your Name for Custom Macropad Configuration
# SPDX-License-Identifier: MIT

from adafruit_hid.keycode import Keycode

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Spaces',     # Application name
    'macros' : [           # List of button macros...
        # COLOR     LABEL       KEY SEQUENCE
        # 1st row ----------
        (0x00FF00, 'breadco', [Keycode.CONTROL, '1']), # Panera green
        (0x0000FF, 'dev', [Keycode.CONTROL, '2']),     # Dark blue
        (0xFFFFFF, 'ai', [Keycode.CONTROL, '3']),      # White
        # 2nd row ----------
        (0xFFFF00, 'datacenter', [Keycode.CONTROL, '4']), # Yellow
        (0x00FF00, 'keeb', [Keycode.CONTROL, '5']),       # Neon
        (0xADD8E6, 'msg', [Keycode.CONTROL, '6']),        # Light blue
        # 3rd row ----------
        (0xFF0000, 'video', [Keycode.CONTROL, '7']),    # Red
        (0xFFC0CB, 'audio', [Keycode.CONTROL, '8']),    # Pink
        (0x800080, 'mail', [Keycode.CONTROL, '9']),     # Purple
        # 4th row ----------
        (0x008080, 'consume', [Keycode.CONTROL, '0']),  # Teal
        (0xFFA500, 'maker', [Keycode.CONTROL, 'K']),    # Orange
        (0xFFFF00, 'moto', [Keycode.CONTROL, 'M'])      # Solar
    ]
}
