"""
This module handles the menu display and navigation for the MacroPad.
"""

import time
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label

MENU_ITEMS = 5  # Number of menu items to display (odd number)

def show_menu(macropad, items, current_item, inverse=False):
    """
    Display the menu on the MacroPad's screen.
    """
    menu_group = displayio.Group()

    # Calculate the range of items to display
    total_items = len(items)
    half_display = MENU_ITEMS // 2
    start_index = max(0, min(current_item - half_display, total_items - MENU_ITEMS))
    end_index = min(start_index + MENU_ITEMS, total_items)

    # Create labels for the visible items
    for i in range(start_index, end_index):
        is_selected = (i == current_item)
        item = items[i]
        text = item[0] if isinstance(item, tuple) else item.name
        if isinstance(item, tuple):
            text = f"[{text}]"  # Indicate folders with brackets
        y_position = ((i - start_index) * 12) + 6  # Center text vertically in each row
        
        if is_selected:
            # Add background for selected item
            selected_bg = Rect(0, (i - start_index) * 12, macropad.display.width, 12, fill=0x000000 if inverse else 0xFFFFFF)
            menu_group.append(selected_bg)
        
        menu_label = label.Label(
            terminalio.FONT,
            text=text,
            color=0xFFFFFF if (inverse and is_selected) else (0x000000 if is_selected else 0xFFFFFF),
            anchored_position=(macropad.display.width - 1, y_position),
            anchor_point=(1.0, 0.5)  # Right-align the text
        )
        menu_group.append(menu_label)

    macropad.display.root_group = menu_group
    macropad.display.refresh()

def flash_selected(macropad, items, current_item):
    """
    Flash the selected item in the menu.
    """
    for _ in range(2):  # Flash 2 times
        show_menu(macropad, items, current_item, inverse=True)
        time.sleep(0.05)
        show_menu(macropad, items, current_item, inverse=False)
        time.sleep(0.05)

def navigate_menu(macropad, items):
    """
    Navigate the menu and return the selected item.
    """
    current_item = 0
    show_menu(macropad, items, current_item)
    menu_timeout = time.monotonic() + 3
    last_encoder_position = macropad.encoder

    while True:
        macropad.encoder_switch_debounced.update()
        current_encoder_position = macropad.encoder
        
        if current_encoder_position != last_encoder_position:
            # Encoder turned, update selection
            current_item = (current_item + current_encoder_position - last_encoder_position) % len(items)
            show_menu(macropad, items, current_item)
            menu_timeout = time.monotonic() + 3  # Reset timeout
            last_encoder_position = current_encoder_position

        if macropad.encoder_switch_debounced.pressed:
            # Selection made
            flash_selected(macropad, items, current_item)
            return items[current_item]

        if time.monotonic() > menu_timeout:
            # Timeout, return None
            return None

        time.sleep(0.01)  # Small delay to prevent excessive CPU usage