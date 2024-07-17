"""
This module handles the execution of macros based on key events.
"""

import time

def handle_key_event(macropad, app, event):
    """
    Handle a key event for the given app.
    """
    key_number = event.key_number
    pressed = event.pressed

    if key_number < len(app.macros):
        sequence = app.macros[key_number][2]
        if pressed:
            if key_number < 12:  # No pixel for encoder button
                macropad.pixels[key_number] = 0xFFFFFF
                macropad.pixels.show()
            execute_sequence(macropad, sequence)
        else:
            release_sequence(macropad, sequence)
            if key_number < 12:  # No pixel for encoder button
                macropad.pixels[key_number] = app.macros[key_number][0]
                macropad.pixels.show()

def execute_sequence(macropad, sequence):
    """
    Execute a macro sequence.
    """
    for item in sequence:
        if isinstance(item, int):
            if item >= 0:
                macropad.keyboard.press(item)
            else:
                macropad.keyboard.release(-item)
        elif isinstance(item, float):
            time.sleep(item)
        elif isinstance(item, str):
            macropad.keyboard_layout.write(item)
        elif isinstance(item, list):
            for code in item:
                if isinstance(code, int):
                    macropad.consumer_control.release()
                    macropad.consumer_control.press(code)
                if isinstance(code, float):
                    time.sleep(code)
        elif isinstance(item, dict):
            if 'buttons' in item:
                if item['buttons'] >= 0:
                    macropad.mouse.press(item['buttons'])
                else:
                    macropad.mouse.release(-item['buttons'])
            macropad.mouse.move(item['x'] if 'x' in item else 0,
                                item['y'] if 'y' in item else 0,
                                item['wheel'] if 'wheel' in item else 0)
            if 'tone' in item:
                if item['tone'] > 0:
                    macropad.stop_tone()
                    macropad.start_tone(item['tone'])
                else:
                    macropad.stop_tone()
            elif 'play' in item:
                macropad.play_file(item['play'])

def release_sequence(macropad, sequence):
    """
    Release any still-pressed keys, consumer codes, mouse buttons.
    """
    for item in sequence:
        if isinstance(item, int):
            if item >= 0:
                macropad.keyboard.release(item)
        elif isinstance(item, dict):
            if 'buttons' in item:
                if item['buttons'] >= 0:
                    macropad.mouse.release(item['buttons'])
            elif 'tone' in item:
                macropad.stop_tone()
    macropad.consumer_control.release()