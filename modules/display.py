"""
This module handles the setup and management of the MacroPad's display.
"""

import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

def setup_display(macropad):
    """
    Set up the displayio group with all the labels for the MacroPad's display.
    """
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
    return group

def show_group(macropad, group):
    """
    Set the root group of the display and refresh it.
    """
    macropad.display.root_group = group
    macropad.display.refresh()