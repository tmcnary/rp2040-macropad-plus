# MacroPad Hotkeys "Enhanced"

## Author

Tony Bologna

## Description

This project is an enhanced version of the MacroPad Hotkeys example from the [Adafruit Learning System Guide](https://learn.adafruit.com/macropad-hotkeys). It extends the functionality of the original example to provide a more feature-rich and flexible macro system for the Adafruit MacroPad RP2040.

## Features

- **Dynamic Macro Loading**: Automatically loads macro files from the `/macros` folder, including support for subfolders.
- **Menu Navigation**: Provides an intuitive menu system for selecting macro sets using the MacroPad's rotary encoder.
- **Favorites System**: Allows users to set and quickly access their most-used macros.
- **Tap Dance Functionality**: Implements advanced key press behaviors, allowing multiple actions per key based on tap count and hold duration:
  - Single Tap
  - Double Tap
  - Hold
  - Tap and Hold
- **Modular Structure**: Code is organized into separate modules for easier maintenance and extensibility.

## Project Structure

```
/
├── code.py                 # Main entry point
├── lib/                    # CircuitPython libraries
├── modules/                # Custom modules
│   ├── macropad_handler.py # Handles MacroPad operations
│   ├── menu_handler.py     # Manages menu display and navigation
│   ├── favorites_handler.py# Handles favorite macros
│   ├── tap_dance.py        # Implements tap dance functionality
│   └── utils.py            # Utility constants and functions
└── macros/                 # Folder for macro files
    └── preferences/        # Subfolder for preference-related macros
        └── favorites.py    # Favorites macro file
```

## Setup and Usage

1. Ensure your MacroPad has the latest version of CircuitPython installed.
2. Copy the contents of this project to the root of your MacroPad's filesystem.
3. Create your macro files in the `/macros` folder. You can organize them into subfolders if desired.
4. Power on your MacroPad. The main menu will display available macro sets.
5. Use the rotary encoder to navigate through macro sets and press it to select.
6. Press keys to execute macros. Use tap dance features for advanced functionality.

## Customization

- Modify existing macro files or create new ones in the `/macros` folder.
- Adjust timing constants in `tap_dance.py` to change tap dance behavior.
- Modify `favorites_handler.py` to change how favorites are stored and accessed.

## Dependencies

This project requires CircuitPython and the following libraries:

- adafruit_macropad
- adafruit_display_text
- adafruit_display_shapes

Ensure these are present in the `lib` folder of your MacroPad.

## Contributing

Feel free to fork this project and submit pull requests for any enhancements or bug fixes. Please maintain the existing code style and add appropriate documentation for new features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

This project is a derivative work based on the MacroPad Hotkeys example from the Adafruit Learning System Guide. Special thanks to the Adafruit team for their original work and excellent documentation.

## Disclaimer

This code is provided as-is, without any warranty. Use at your own risk.
