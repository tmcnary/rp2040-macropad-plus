"""
Menu Handler Module

This module provides a handler class for managing the menu display and navigation
on the Adafruit MacroPad.

Classes:
- MenuHandler: Handles menu display and navigation.

Author: YourName
Date: YYYY-MM-DD
License: MIT
"""

import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

class MenuHandler:
    """
    Handles menu display and navigation for the MacroPad.

    Attributes:
        macropad: The MacroPad object.
        handler: The MacroPadHandler object.
        MENU_ITEMS (int): Number of menu items to display at once.

    Methods:
        show_menu: Displays the menu on the MacroPad's screen.
        flash_selected: Flashes the selected menu item.
        navigate_menu: Handles menu navigation and selection.
    """

    def __init__(self, macropad, handler):
        """
        Initializes the MenuHandler.

        Args:
            macropad: The MacroPad object.
            handler: The MacroPadHandler object.
        """
        self.macropad = macropad
        self.handler = handler
        self.MENU_ITEMS = 5

    def show_menu(self, items, current_item, inverse=False):
        """
        Displays the menu on the MacroPad's screen.

        Args:
            items (list): List of menu items to display.
            current_item (int): Index of the currently selected item.
            inverse (bool): Whether to invert the colors for the selected item.
        """
        menu_group = displayio.Group()
        total_items = len(items)
        half_display = self.MENU_ITEMS // 2
        start_index = max(0, min(current_item - half_display, total_items - self.MENU_ITEMS))
        end_index = min(start_index + self.MENU_ITEMS, total_items)

        for i in range(start_index, end_index):
            is_selected = (i == current_item)
            item = items[i]
            text = item[0] if isinstance(item, tuple) else item.name
            if isinstance(item, tuple):
                text = f"[{text}]"
            y_position = ((i - start_index) * 12) + 6
            
            if is_selected:
                selected_bg = Rect(0, (i - start_index) * 12, self.macropad.display.width, 12, fill=0x000000 if inverse else 0xFFFFFF)
                menu_group.append(selected_bg)
            
            menu_label = label.Label(
                terminalio.FONT,
                text=text,
                color=0xFFFFFF if (inverse and is_selected) else (0x000000 if is_selected else 0xFFFFFF),
                anchored_position=(self.macropad.display.width - 1, y_position),
                anchor_point=(1.0, 0.5)
            )
            menu_group.append(menu_label)

        self.macropad.display.root_group = menu_group
        self.macropad.display.refresh()

    def flash_selected(self, items, current_item):
        """
        Flashes the selected menu item.

        Args:
            items (list): List of menu items.
            current_item (int): Index of the currently selected item.
        """
        for _ in range(2):
            self.show_menu(items, current_item, inverse=True)
            time.sleep(0.05)
            self.show_menu(items, current_item, inverse=False)
            time.sleep(0.05)

    def navigate_menu(self, items):
        """
        Handles menu navigation and selection.

        Args:
            items (list): List of menu items to navigate.

        Returns:
            The selected menu item or None if no selection was made.
        """
        current_item = 0
        self.show_menu(items, current_item)
        menu_timeout = time.monotonic() + 3
        last_encoder_position = self.macropad.encoder

        while True:
            self.macropad.encoder_switch_debounced.update()
            current_encoder_position = self.macropad.encoder
            
            if current_encoder_position != last_encoder_position:
                current_item = (current_item + current_encoder_position - last_encoder_position) % len(items)
                self.show_menu(items, current_item)
                menu_timeout = time.monotonic() + 3
                last_encoder_position = current_encoder_position

            if self.macropad.encoder_switch_debounced.pressed:
                self.flash_selected(items, current_item)
                return items[current_item]

            if time.monotonic() > menu_timeout:
                return None

            time.sleep(0.01)