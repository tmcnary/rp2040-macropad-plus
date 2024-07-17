# 🎛️ MacroPad Hotkeys Project

Welcome to the MacroPad Hotkeys Project! This project turns your Adafruit MacroPad into a customizable macro keyboard with a user-friendly menu system.

## 📁 Directory Structure

```plaintext
/macropad_hotkeys
├── 📂 lib (CircuitPython libraries)
├── 📂 macros (Your macro files go here)
├── 📂 modules
│   ├── __init__.py
│   ├── app.py (App class and file reader)
│   ├── display.py (Display setup and management)
│   ├── macro_handler.py (Macro execution handler)
│   └── menu.py (Menu navigation)
├── code.py (Main script)
└── README.md (You are here!)
```

## 🚀 Features

- 📊 Easy-to-use menu system for selecting macros
- 📁 Support for organizing macros in folders
- 🔄 Dynamic macro switching with encoder rotation
- 💡 Visual feedback with LED indicators

## 🛠️ How to Build a Macro

Creating a macro is simple! Here's an example of how to build a macro file:

1. Create a new `.py` file in the `/macros` folder (e.g., `my_macro.py`)
2. Define your macro as follows:

    ```python
    app = {
        'name' : 'My Macro',  # Name displayed in the menu
        'macros' : [
            # COLOR    LABEL    KEY SEQUENCE
            (0x004000, 'Hello', ['Hello, World!\n']),
            (0x400000, 'Ctrl+C', [{'buttons':1}, 'c', -{'buttons':1}]),
            (0x202000, 'Alt+F4', [{'buttons':4}, {'buttons':1}, 'f4', -{'buttons':1}, -{'buttons':4}]),
            # Add up to 12 macros here
        ]
    }
    ```

3. Save the file and restart your MacroPad

Each macro in the list consists of three elements:

1. Color: An RGB color value for the key's LED
2. Label: The text displayed on the OLED for this key
3. Key Sequence: A list of actions to perform when the key is pressed

## 🌈 Color Reference

Here's a quick reference for some common colors:

- 🔴 Red: `0xFF0000`
- 🟢 Green: `0x00FF00`
- 🔵 Blue: `0x0000FF`
- 🟡 Yellow: `0xFFFF00`
- 🟣 Purple: `0x800080`
- ⚪ White: `0xFFFFFF`

## 🔧 Customization

Feel free to modify the `code.py` file and the modules to add new features or change the behavior of your MacroPad. The modular structure makes it easy to extend and maintain the project.

## 📚 Additional Resources

- [Adafruit MacroPad Documentation](https://learn.adafruit.com/adafruit-macropad-rp2040)
- [CircuitPython Documentation](https://docs.circuitpython.org/)

Happy coding! 🎉
