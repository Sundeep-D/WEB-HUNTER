"""
File: web-hunter.py
Author: Sundeep Dayalan
Website: www.sundeepdayalan.in
Github: https://github.com/Sundeep-D/WEB-HUNTER
Date: April 20, 2023

Description: This code sets up a GUI application with a navigation drawer and two frames using the customtkinter and
PIL modules and functions from the ENGINE and UI packages. The App class inherits from customtkinter.CTk and
initializes the UI using functions from the UI_handler module. It then configures a 2x2 grid layout, sets up the
navigation drawer and frames, and sets default values."""
import customtkinter
from PIL import Image

from ENGINE.export import export
from UI import UI_handler

from UI.UI_handler import initialize_ui, configure_grid, configure_navigation_drawer, \
    render_navigation_drawer_items, configure_home_frame, configure_about_frame, render_home_frame, set_default_values, \
    listen_key_entries


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        UI_handler.root = self
        initialize_ui()

        # configure grid layout (2X2)
        configure_grid()
        configure_navigation_drawer()
        render_navigation_drawer_items()
        configure_home_frame()
        configure_about_frame()
        render_home_frame()
        set_default_values()
        listen_key_entries(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
