"""
File: ScrollableHomeFrame.py
Author: Sundeep Dayalan
Website: www.sundeepdayalan.in
Github: https://github.com/Sundeep-D/WEB-HUNTER
Date: April 28, 2023

Description: This code defines a class ScrollableHomeFrame that extends a custom scrollbar frame widget. It provides
methods to add different types of items to the frame, such as text labels, headers, and links. It also includes a
function openlink that opens a web link in the default browser."""
import io
import os
import urllib
import webbrowser

from PIL import Image, ImageTk

import customtkinter


def openlink(item):
    print("Opening... ", item)
    webbrowser.open_new(item)
    pass


class ScrollableHomeFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.who_is_icon = None
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18), weight=2)
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):

        label = customtkinter.CTkLabel(self, text=item, compound="left", padx=5, anchor="w",
                                       font=customtkinter.CTkFont(size=15))
        label.grid(row=len(self.label_list), column=0, pady=(10, 10), sticky="w")
        self.label_list.append(label)

    def add_whois_item(self, item, image=None):

        # #8696E1
        icon = "id.png"
        if ('asn' in item):
            icon = "id.png"
        if ('cidr' in item or 'query' in item or 'query' in item):
            icon = "ip.png"
        if ('country' in item or 'state' in item):
            icon = "location.png"
        if ('name' in item):
            icon = "name.png"
        if ('description' in item):
            icon = "info.png"
        if ('date' in item):
            icon = "date.png"

        if item.strip():
            self.who_is_icon = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, icon)), size=(20, 20))
            label = customtkinter.CTkLabel(self, text=item, padx=25, anchor="w", font=customtkinter.CTkFont(size=15),
                                           image=self.who_is_icon, compound="left")
        else:
            label = customtkinter.CTkLabel(self, text=item, padx=25, anchor="w", font=customtkinter.CTkFont(size=15),
                                           )

        label.grid(row=len(self.label_list), column=0, pady=(10, 10), sticky="w")
        self.label_list.append(label)

    def add_headers_item(self, item, image=None):

        if not item:
            label = customtkinter.CTkLabel(self, text=' ', compound="left", padx=5, anchor="w",
                                           font=customtkinter.CTkFont(size=15))
            label.grid(row=len(self.label_list), column=0, pady=(10, 10), sticky="w")
            self.label_list.append(label)

        else:
            # Create a Frame widget
            frame = customtkinter.CTkFrame(self, fg_color="transparent")
            frame.grid(row=len(self.label_list), column=0, pady=(5, 10), padx=(20, 10), sticky="we")
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

    def add_links_item(self, item):

        if not item:
            label = customtkinter.CTkLabel(self, text=' ', compound="left", padx=5, anchor="w",
                                           font=customtkinter.CTkFont(size=15))
            label.grid(row=len(self.label_list), column=0, pady=(10, 10), sticky="w")
            self.label_list.append(label)

        else:
            # Create a Frame widget
            frame = customtkinter.CTkFrame(self, fg_color="transparent")
            frame.grid(row=len(self.label_list), column=0, pady=(15, 10), padx=(20, 10), sticky="we")
            frame.grid_rowconfigure(1, weight=1)
            # frame.grid_columnconfigure(1, weight=1)
            # frame.grid_columnconfigure(2, weight=1)

            # Create the label widget and add it to the Frame
            link_icon = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, 'link.png')), size=(20, 20))
            label = customtkinter.CTkLabel(frame, text="", padx=25, anchor="w", font=customtkinter.CTkFont(size=15),
                                           image=link_icon, compound="left")
            label.grid(row=0, column=0, sticky="w")

            link = customtkinter.CTkLabel(frame, text=item, compound="left", padx=5, anchor="w",
                                          font=customtkinter.CTkFont(size=15))
            link.grid(row=0, column=1, sticky="w")

            link_open_icon = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, 'open.png')),
                                                    size=(15, 15))
            open_link = customtkinter.CTkButton(frame, text='', fg_color="transparent", width=20,
                                                command=lambda: openlink(item), image=link_open_icon, compound="left")
            open_link.grid(row=0, column=2, sticky="w")

            # Add the label widget to the label_list
            self.label_list.append(frame)

    def add_image(self, item, i):
        row = i // 6
        col = i % 6

        try:
            image_data = urllib.request.urlopen(item).read()

            # Create a PIL image object from the image data
            image = Image.open(io.BytesIO(image_data))
            resized_image = image.resize((100, 100))

            # Create a PhotoImage object from the PIL image
            photo_image = ImageTk.PhotoImage(resized_image)

        except Exception as e:
            print("Error loading image:", e)
            print("Image url:", item)
            image = Image.open(os.path.join(self.image_path, 'error.png'))
            resized_image = image.resize((100, 100))
            photo_image = ImageTk.PhotoImage(resized_image)

        label = customtkinter.CTkLabel(self, image=photo_image, text='', compound="left", padx=5, anchor="w",
                                       font=customtkinter.CTkFont(size=15))
        label.grid(row=row, column=col, padx=(0, 0), pady=(10, 10), sticky="nesw")
        self.label_list.append(label)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return

    def add_ports_item(self, item, image=None):

        # #8696E1
        icon = "port.png"

        if item.strip():
            self.who_is_icon = customtkinter.CTkImage(Image.open(os.path.join(self.image_path, icon)), size=(20, 20))
            label = customtkinter.CTkLabel(self, text=item, padx=25, anchor="w", font=customtkinter.CTkFont(size=15),
                                           image=self.who_is_icon, compound="left")
        else:
            label = customtkinter.CTkLabel(self, text=item, padx=25, anchor="w", font=customtkinter.CTkFont(size=15),
                                           )

        label.grid(row=len(self.label_list), column=0, pady=(10, 10), sticky="w")
        self.label_list.append(label)


    def add_about_information(self, item):

        if not item:
            label = customtkinter.CTkLabel(self, text=' ', compound="left", padx=5, anchor="w",
                                           font=customtkinter.CTkFont(size=15))
            label.grid(row=len(self.label_list), column=0, pady=(10, 10), sticky="w")
            self.label_list.append(label)

        else:
            # Create a Frame widget
            frame = customtkinter.CTkFrame(self, fg_color="transparent")
            frame.grid(row=len(self.label_list), column=0, pady=(5, 10), padx=(20, 10), sticky="we")
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
