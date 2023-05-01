# Sundeep Dayalan
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
