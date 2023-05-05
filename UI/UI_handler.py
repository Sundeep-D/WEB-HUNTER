import os
import re
import time
import customtkinter
from PIL import Image
from ENGINE import scanner
from ENGINE.export import export
from ENGINE.initializer import initialize_scanner
from ENGINE.scanner import perform_full_scan
from tkinter import messagebox

from UI.ScrollableAboutFrame import ScrollableAboutFrame
from UI.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame

root = None
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
results_db = {}
isScanning = False


def initialize_ui():
    root.geometry("1100x580")

    # Set window title
    root.title("Web Hunter")
    # root.attributes('-fullscreen', True)
    root.wm_state('zoomed')
    root.update()
    root.attributes('-fullscreen', False)
    # root.wm_iconbitmap('UI/images/logo.ico')

    customtkinter.set_appearance_mode(
        "System"
    )  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme(
        "dark-blue"
    )  # Themes: "blue" (standard), "green", "dark-blue"


def configure_grid():
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)


def configure_navigation_drawer():
    root.sidebar_frame = customtkinter.CTkFrame(root, width=140, corner_radius=0)
    root.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
    root.sidebar_frame.grid_rowconfigure(4, weight=1)


def render_navigation_drawer_items():
    root.scan_image = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(image_path, "scan_light.png")),
        dark_image=Image.open(os.path.join(image_path, "scan_dark.png")),
        size=(20, 20),
    )
    root.chat_image = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
        dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
        size=(20, 20),
    )

    root.export_image = customtkinter.CTkImage(
        light_image=Image.open(os.path.join(image_path, "export_light.png")),
        dark_image=Image.open(os.path.join(image_path, "export_dark.png")),
        size=(20, 20),
    )

    root.home_button = customtkinter.CTkButton(
        root.sidebar_frame,
        corner_radius=0,
        height=40,
        border_spacing=10,
        text="Scan",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover_color=("gray70", "gray30"),
        image=root.scan_image,
        anchor="w",
        command=home_button_event,
    )
    root.home_button.grid(row=1, column=0, sticky="ew")

    root.about_button = customtkinter.CTkButton(
        root.sidebar_frame,
        corner_radius=0,
        height=40,
        border_spacing=10,
        text="About",
        fg_color="transparent",
        text_color=("gray10", "gray90"),
        hover_color=("gray70", "gray30"),
        image=root.chat_image,
        anchor="w",
        command=frame_2_button_event,
    )
    root.about_button.grid(row=2, column=0, sticky="ew")

    root.logo_label = customtkinter.CTkLabel(
        root.sidebar_frame,
        text="WEB HUNTER",
        font=customtkinter.CTkFont(size=20, weight="bold"),
    )
    root.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

    # root.appearance_mode_label = customtkinter.CTkLabel(
    #     root.sidebar_frame, text="Appearance Mode:", anchor="w"
    # )
    # root.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
    root.export_button = customtkinter.CTkButton(
        root.sidebar_frame,
        text="Export results",
        image=root.export_image,
        command=export_results
    )
    root.export_button.grid(row=5, column=0, padx=20, pady=(120, 10))

    root.new_scan_button = customtkinter.CTkButton(
        root.sidebar_frame,
        text="New Scan",
        image=root.scan_image,
        command=initialize_new_scan
    )
    root.new_scan_button.grid(row=5, column=0, padx=20, pady=(10, 10))
    root.new_scan_button.grid_remove()
    root.export_button.grid_remove()

    root.appearance_mode_option_menu = customtkinter.CTkOptionMenu(
        root.sidebar_frame,
        values=["Light", "Dark", "System"],
        command=change_appearance_mode_event,
    )
    root.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 10))
    # set_default_values(root)


def configure_home_frame():
    root.home_frame = customtkinter.CTkFrame(
        root, corner_radius=0, fg_color="transparent"
    )
    # root.home_frame.grid_columnconfigure(0, weight=1)
    root.home_frame.grid_columnconfigure(1, weight=1)
    root.home_frame.grid_columnconfigure((2), weight=16)
    root.home_frame.grid_rowconfigure((0), weight=0)
    root.home_frame.grid_rowconfigure((1, 2), weight=2)

    print(dir(root.home_frame))
    #     bg
    root.home_frame.bg_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "bg.png")),
                                                      size=(1200, 800))
    root.home_frame.bg_image_label = customtkinter.CTkLabel(root.home_frame, image=root.home_frame.bg_image, text='')
    root.home_frame.bg_image_label.grid(row=0, column=2, rowspan=6, columnspan=2, padx=(5, 5), pady=(10, 5),
                                        sticky="nsew")
    root.home_frame.bg_image_label.grid()
    # self.bg_image_label.grid_remove()


def configure_about_frame():
    root.about_frame = customtkinter.CTkFrame(
        root, corner_radius=0, fg_color="transparent"
    )
    # root.about_frame.progressbar_1 = customtkinter.CTkProgressBar(root.about_frame)
    # root.about_frame.progressbar_1.grid(
    #     row=2,
    #     column=1,
    #     rowspan=1,
    #     columnspan=2,
    #     padx=(20, 10),
    #     pady=(10, 10),
    #     sticky="ew",
    # )
    render_about_frame()


def render_home_frame():
    root.url_info = customtkinter.CTkLabel(
        root.home_frame, text="Initializing...", font=customtkinter.CTkFont(size=15)
    )
    root.url_info.grid(
        row=0,
        column=1,
        rowspan=1,
        columnspan=2,
        padx=(20, 0),
        pady=(20, 20),
        sticky="new",
    )
    root.url_info.grid_remove()

    root.url_input = customtkinter.CTkEntry(
        root.home_frame, placeholder_text="https://google.com", font=(None, 40)
    )
    root.url_input.grid(
        row=2,
        column=1,
        rowspan=1,
        columnspan=2,
        padx=(30, 0),
        pady=(240, 0),
        sticky="ew",
    )

    root.main_button_1 = customtkinter.CTkButton(
        master=root.home_frame,
        fg_color="transparent",
        border_width=2,
        text_color=("gray10", "#DCE4EE"),
        height=50,
        text="Scan",
        command=perform_scan,
    )

    root.main_button_1.grid(
        row=2, column=3, rowspan=1, padx=(20, 20), pady=(240, 0), sticky="ew"
    )

    root.progress_status = customtkinter.CTkLabel(
        root.home_frame, text="Initializing...", font=customtkinter.CTkFont(size=15)
    )
    root.progress_status.grid(
        row=2, rowspan=2, column=1, columnspan=2, padx=20, pady=(360, 20)
    )
    root.progress_status.grid_remove()

    # root.url_input.grid_remove()
    # root.main_button_1.grid_remove()

    # create tabview
    root.tabview = customtkinter.CTkTabview(root.home_frame, width=250)
    root.tabview.grid(
        row=1,
        column=2,
        rowspan=3,
        columnspan=2,
        padx=(20, 20),
        pady=(0, 10),
        sticky="nsew",
    )
    root.tabview.add("Whois")
    root.tabview.add("Headers")
    root.tabview.add("DNS")
    root.tabview.add("External urls")
    root.tabview.add("Internal urls")
    root.tabview.add("Images")
    root.tabview.add("Ports")
    root.tabview.add("SSL")

    root.tabview.grid_remove()
    root.progressbar_1 = customtkinter.CTkProgressBar(root.home_frame)
    root.progressbar_1.grid(
        row=2,
        column=1,
        rowspan=1,
        columnspan=2,
        padx=(20, 10),
        pady=(250, 10),
        sticky="ew",
    )
    root.progressbar_1.grid_remove()


def set_default_values():
    root.appearance_mode_option_menu.set("Dark")
    select_frame_by_name("home")


def start_scan():
    root.url_input.grid_remove()
    root.progressbar_1.grid()
    root.progressbar_1.set(0)
    root.main_button_1.configure(text="Stop")
    root.main_button_1.update()
    root.progress_status.grid()
    root.progress_status.configure(text="Initializing scanner...", text_color="gray")
    root.progress_status.update()


def stop_scan():
    root.url_input.grid()
    root.main_button_1.configure(text="Scan")
    root.main_button_1.update()
    root.progressbar_1.grid_remove()
    root.progress_status.grid_remove()
    root.home_frame.bg_image_label.grid()


def change_appearance_mode_event(new_appearance_mode: str):
    customtkinter.set_appearance_mode(new_appearance_mode)


def home_button_event():
    select_frame_by_name("home")


def frame_2_button_event():
    select_frame_by_name("about")


def select_frame_by_name(name):
    # set button color for selected button
    root.home_button.configure(
        fg_color=("gray75", "gray25") if name == "home" else "transparent"
    )
    root.about_button.configure(
        fg_color=("gray75", "gray25") if name == "frame_2" else "transparent"
    )

    # show selected frame
    if name == "home":
        root.home_frame.grid(row=0, column=1, sticky="nsew")
    else:
        root.home_frame.grid_forget()

    if name == "about":
        root.about_frame.grid(row=0, column=1, sticky="nsew")
    else:
        root.about_frame.grid_forget()


def listen_key_entries(self):
    root.bind("<Return>", on_return_key_press)


def on_return_key_press(event):
    perform_scan()


def perform_scan():
    global isScanning
    global results_db
    if isScanning:
        isScanning = False
        scanner.isScanningInProgress = False
        # stop the scan
        stop_scan()
    else:
        isScanning = True
        scanner.isScanningInProgress = True
        results_db = {}
        # start the scan
        url = root.url_input.get()
        print(url)
        # url = "https://googler.innn/"
        if validate_url(url):
            print("Valid URL")
            root.main_button_1.focus_set()

            initialize_scanner(root, url, results_db)
            if 'ip' in results_db:
                start_scan()
                time.sleep(1)
                print("INITIAL DATA: ", results_db)

                perform_full_scan(root, results_db, url)
            else:
                print("Scan aborted due to invalid url")
                initialize_new_scan()


        else:
            print("Invalid URL")
            root.url_input.delete(0, customtkinter.END)
            root.main_button_1.focus_set()
            messagebox.showinfo(title="Invalid Url", message="The url you entered is invalid")


def validate_url(url):
    regex = re.compile(
        r"^(?:http|ftp)s?://"  # scheme
        r"(?:\S+(?::\S*)?@)?(?:[\w-]+\.)+[\w]{2,}"  # domain
        r"(?:\:\d{1,5})?"  # port
        r"(?:/[\w\-\.~!$&'()*+,;=:@/]*)?"  # path
        r"(?:\?[^\s]*)?"  # query string
        r"(?:#[^\s]*)?$"  # fragment
        , re.IGNORECASE)
    return regex.match(url) is not None


def initialize_new_scan():
    root.url_input.grid()
    root.main_button_1.grid()
    root.progressbar_1.grid_remove()
    root.progress_status.grid_remove()
    root.tabview.grid_remove()
    root.url_info.grid_remove()
    root.home_frame.bg_image_label.grid()
    root.main_button_1.focus_set()
    root.new_scan_button.grid_remove()
    root.export_button.grid_remove()


def export_results():
    export(results_db)


def render_about_frame():
    root.scrollable_about_frame = ScrollableAboutFrame(root.about_frame)
    content_list = ["Designed and developed by:Sundeep Dayalan",
                    "Software name:WEB HUNTER",
                    "Description:This project aims to develop an automated web reconnaissance software using Python. The software will provide a comprehensive overview of a target website by integrating multiple functionalities into a single application. It will include features such as DNS enumeration, Whois lookup, SSL certificate details, crawling, subdomain enumeration, directory searching, Wayback Machine integration, port scanning, and exporting results to a text file. The software will have an attractive Python interface created using PyQT5 and Python Tkinter, and it will be compatible with Windows, Linux, and macOS. The executable file will be generated using Pyinstaller. The goal is to create a reliable and efficient tool that simplifies web reconnaissance tasks for users.",
                    "Disclaimer: This software conducts network scanning activities solely for educational purposes."]
    for i in range(len(content_list)):
        content = f"{content_list[i]}"
        root.scrollable_about_frame.add_about_information(content,root.about_frame)
