"""
Favorites Handler Module

This module provides a handler class for managing favorite macros
on the Adafruit MacroPad.

Classes:
- FavoritesHandler: Handles favorite macro functionality.

Author: YourName
Date: YYYY-MM-DD
License: MIT
"""

import json
from modules.utils import FAVORITES_FILE

class FavoritesHandler:
    """
    Handles favorite macro functionality for the MacroPad.

    Methods:
        load_favorites: Loads favorites from the JSON file.
        save_favorites: Saves favorites to the JSON file.
        set_favorite: Sets a new favorite macro.
        get_favorite: Retrieves a favorite macro.
        handle_favorites: Handles favorite-related actions.
    """

    def load_favorites(self):
        """
        Loads favorites from the JSON file.

        Returns:
            dict: The loaded favorites or an empty dict if the file doesn't exist.
        """
        try:
            with open(FAVORITES_FILE, 'r') as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def save_favorites(self, favorites):
        """
        Saves favorites to the JSON file.

        Args:
            favorites (dict): The favorites to save.
        """
        with open(FAVORITES_FILE, 'w') as f:
            json.dump(favorites, f)

    def set_favorite(self, key, app):
        """
        Sets a new favorite macro.

        Args:
            key (int): The key number to associate with the favorite.
            app (App): The app to set as a favorite.
        """
        favorites = self.load_favorites()
        favorites[str(key)] = {'name': app.name, 'filename': app.filename, 'folder': app.folder}
        self.save_favorites(favorites)

    def get_favorite(self, key, apps):
        """
        Retrieves a favorite macro.

        Args:
            key (int): The key number of the favorite to retrieve.
            apps (list): List of available apps.

        Returns:
            App: The favorite app if found, None otherwise.
        """
        favorites = self.load_favorites()
        if str(key) in favorites:
            fav = favorites[str(key)]
            for app in apps:
                if isinstance(app, App) and app.filename == fav['filename'] and app.folder == fav['folder']:
                    return app
        return None

    def handle_favorites(self, handler, current_app, key_number, pressed, setting_favorite):
        """
        Handles favorite-related actions.

        Args:
            handler (MacroPadHandler): The MacroPadHandler object.
            current_app (App): The current active app.
            key_number (int): The pressed key number.
            pressed (bool): Whether the key is pressed or released.
            setting_favorite (bool): Whether we're currently setting a favorite.

        Returns:
            bool: The updated setting_favorite status.
        """
        if pressed:
            sequence = current_app.macros[key_number][2]
            if sequence[0] == 'SET_FAVORITE':
                setting_favorite = True
                handler.show_message('Set Favorite', 1)
            elif sequence[0] == 'BACK_TO_MAIN':
                main_app = handler.read_macro_files()[0]
                if isinstance(main_app, tuple):
                    main_app = main_app[1][0]
                handler.switch_app(main_app)
            elif sequence[0].startswith('FAVORITE_'):
                fav_num = int(sequence[0].split('_')[1])
                fav_app = self.get_favorite(fav_num - 1, handler.read_macro_files())
                if fav_app:
                    handler.switch_app(fav_app)
        return setting_favorite