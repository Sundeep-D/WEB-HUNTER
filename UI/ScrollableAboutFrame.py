"""
File: ScrollableAboutFrame.py
Author: Sundeep Dayalan
Website: www.sundeepdayalan.in
Github: https://github.com/Sundeep-D/WEB-HUNTER
Date: May 02, 2023

Description: This code defines a class called ScrollableAboutFrame which is a custom tkinter frame with scrolling
functionality. It contains a method called add_about_information which adds labels and frames to the frame widget
based on input information."""
import os
import customtkinter


class ScrollableAboutFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.who_is_icon = None
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18), weight=2)
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_about_information(self, item, renderframe):

        renderframe.label_list = []
        title = customtkinter.CTkLabel(renderframe, text="WEB HUNTER", compound="left", padx=5, anchor="w",
                                       font=customtkinter.CTkFont(size=35, weight="bold"), text_color="gray")
        title.grid(row=0, column=0, sticky="w")
        if not item:
            label = customtkinter.CTkLabel(renderframe, text=' ', compound="left", padx=5, pady=20, anchor="w",
                                           font=customtkinter.CTkFont(size=15))
            label.grid(row=len(renderframe.label_list), column=0, pady=(10, 10), sticky="w")
            renderframe.label_list.append(label)

        else:
            # Create a Frame widget
            frame = customtkinter.CTkFrame(renderframe, fg_color="transparent")
            frame.grid(row=len(self.label_list), column=0, pady=(45, 10), padx=(20, 10), sticky="we")
            frame.grid_rowconfigure(2, weight=1)

            info = item.split(':')
            # Create the label widget and add it to the Frame
            title = customtkinter.CTkLabel(frame, text=info[0], compound="left", padx=5, anchor="w",
                                           font=customtkinter.CTkFont(size=15, weight="bold"), text_color="gray")
            title.grid(row=0, column=0, sticky="w")

            value = customtkinter.CTkLabel(frame, text=info[1], compound="left", padx=5, anchor="w",
                                           font=customtkinter.CTkFont(size=15))
            value.grid(row=1, column=0, sticky="w")

            # Add the label widget to the label_list
            self.label_list.append(frame)
