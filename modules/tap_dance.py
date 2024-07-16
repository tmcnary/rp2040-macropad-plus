"""
Tap Dance Module

This module provides a handler class for implementing tap dance functionality
on the Adafruit MacroPad, allowing for multiple actions per key based on
tap count and hold duration.

Classes:
- TapDance: Handles tap dance functionality.

Author: YourName
Date: YYYY-MM-DD
License: MIT
"""

import time

class TapDance:
    """
    Handles tap dance functionality for the MacroPad.

    Attributes:
        TAP_DANCE_TIMEOUT (float): Time window for detecting double taps.
        HOLD_TIMEOUT (float): Time threshold for detecting long presses.
        last_press_time (float): Timestamp of the last key press.
        tap_count (int): Number of taps for the current key.
        is_long_press (bool): Whether the current press is a long press.
        current_key (int): The currently pressed key number.

    Methods:
        handle_tap_dance: Handles tap dance actions for a key press/release.
        check_long_press: Checks for long press actions.
    """

    def __init__(self):
        """Initializes the TapDance handler."""
        self.TAP_DANCE_TIMEOUT = 0.3
        self.HOLD_TIMEOUT = 0.5
        self.last_press_time = 0
        self.tap_count = 0
        self.is_long_press = False
        self.current_key = None

    def handle_tap_dance(self, handler, current_app, key_number, pressed):
        """
        Handles tap dance actions for a key press/release.

        Args:
            handler (MacroPadHandler): The MacroPadHandler object.
            current_app (App): The current active app.
            key_number (int): The pressed key number.
            pressed (bool): Whether the key is pressed or released.
        """
        current_time = time.monotonic()
        
        if pressed:
            if current_time - self.last_press_time <= self.TAP_DANCE_TIMEOUT and key_number == self.current_key:
                self.tap_count += 1
            else:
                self.tap_count = 1
            self.last_press_time = current_time
            self.is_long_press = False
            self.current_key = key_number
        else:
            if current_time - self.last_press_time >= self.HOLD_TIMEOUT:
                if self.is_long_press:
                    # Tap and Hold (Action 4)
                    handler.execute_sequence(current_app.macros[key_number][2][3])
                else:
                    # Hold (Action 3)
                    handler.execute_sequence(current_app.macros[key_number][2][2])
            elif self.tap_count == 1:
                # Single Tap (Action 1)
                handler.execute_sequence(current_app.macros[key_number][2][0])
            elif self.tap_count == 2:
                # Double Tap (Action 2)
                handler.execute_sequence(current_app.macros[key_number][2][1])
            
            self.tap_count = 0
            self.is_long_press = False
            self.current_key = None

    def check_long_press(self, handler, current_app):
        """
        Checks for long press actions.

        Args:
            handler (MacroPadHandler): The MacroPadHandler object.
            current_app (App): The current active app.
        """
        current_time = time.monotonic()
        if self.current_key is not None and current_time - self.last_press_time >= self.HOLD_TIMEOUT and not self.is_long_press:
            self.is_long_press = True
            # This will trigger the Hold action when the key is released