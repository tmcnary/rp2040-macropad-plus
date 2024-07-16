# SPDX-FileCopyrightText: 2023 Adafruit Industries
# SPDX-License-Identifier: MIT

from adafruit_hid.keycode import Keycode

app = {
    'name' : 'Favorites',
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, 'Fav1', ['FAVORITE_1']),
        (0x004000, 'Fav2', ['FAVORITE_2']),
        (0x004000, 'Fav3', ['FAVORITE_3']),
        # 2nd row ----------
        (0x004000, 'Fav4', ['FAVORITE_4']),
        (0x004000, 'Fav5', ['FAVORITE_5']),
        (0x004000, 'Fav6', ['FAVORITE_6']),
        # 3rd row ----------
        (0x004000, 'Fav7', ['FAVORITE_7']),
        (0x004000, 'Fav8', ['FAVORITE_8']),
        (0x004000, 'Fav9', ['FAVORITE_9']),
        # 4th row ----------
        (0x400000, 'Set', ['SET_FAVORITE']),
        (0x004000, 'Fav10', ['FAVORITE_10']),
        (0x404000, 'Back', ['BACK_TO_MAIN']),
        # Encoder button ---
        (0x000000, '', [Keycode.BACKSPACE])
    ]
}