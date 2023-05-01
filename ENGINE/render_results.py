import datetime
from tkinter import ttk

import customtkinter

from UI.ScrollableLabelButtonFrame import ScrollableLabelButtonFrame


def render_who_is_information(self, results_db):
    result_array = []

    for key, value in results_db['whois']['result'].items():
        result_array.append(f"{key}: {value}")

    for i in range(1,10):
        result_array.append(f"")

    content_list = result_array

    self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.tabview.tab("Whois"), width=1400,
                                                                    height=900,
                                                                    corner_radius=0)
    self.scrollable_label_button_frame.grid(row=0, column=2, padx=(1, 30), pady=(20, 10), sticky="nsew")

    for i in range(len(content_list)):  # add items with images

        content = f"{content_list[i]}"
        self.scrollable_label_button_frame.add_whois_item(content)


def render_headers_information(self, results_db):
    result_array = []

    for key, value in results_db['headers']['result'].items():
        result_array.append(f"{key}: {value}")

    for i in range(1,10):
        result_array.append(f"")

    print("HEADERS: len(content_list): ",len(result_array))
    content_list = result_array

    self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.tabview.tab("Headers"), width=1400,
                                                                    height=900,
                                                                    corner_radius=0)
    self.scrollable_label_button_frame.grid(row=0, column=2, padx=(1, 30), pady=(20, 10), sticky="nsew")
    for i in range(len(content_list)):
        content = f"{content_list[i]}"
        self.scrollable_label_button_frame.add_headers_item(content)


def render_ssl_information(self, results_db):
    result_array = []

    for key, value in results_db['ssl']['result'].items():
        result_array.append(f"{key}: {value}")

    for i in range(1,10):
        result_array.append(f"")

    content_list = result_array

    self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.tabview.tab("SSL"), width=1400,
                                                                    height=900,
                                                                    corner_radius=0)
    self.scrollable_label_button_frame.grid(row=0, column=2, padx=(1, 30), pady=(20, 10), sticky="nsew")
    for i in range(len(content_list)):
        content = f"{content_list[i]}"
        self.scrollable_label_button_frame.add_headers_item(content)


def render_dns_information(self, results_db):
    content_list = results_db['dns']['result']

    style = ttk.Style()

    style.theme_use("default")

    style.configure("Treeview",
                    background="#2a2d2e",
                    foreground="#ffffff",
                    rowheight=25,
                    fieldbackground="white",
                    bordercolor="#fffff",
                    borderwidth=0)
    style.map('Treeview', background=[('selected', '#ffffff')])
    style.map('Treeview', foreground=[('selected', '#000000')])

    style.configure("Treeview.Heading",
                    background="#565b5e",
                    foreground="white",
                    relief="flat")
    style.map("Treeview.Heading",
              background=[('active', 'white')])

    self.frame_right = ScrollableLabelButtonFrame(master=self.tabview.tab("DNS"), width=1400,
                                                  height=4000,
                                              corner_radius=0)
    self.frame_right.grid(row=0, column=2, padx=(1, 30), pady=(20, 100), sticky="nsew")

    columns = ('sno','name', 'ttl', 'class_', 'type_','address')

    self.table = ttk.Treeview(master=self.frame_right,
                              columns=columns,
                              height=117,
                              selectmode='browse',
                              show='headings')

    # Get the screen width
    screen_width = self.winfo_screenwidth()
    # Calculate the column widths based on the screen width
    column1_width = int((50 * screen_width) / 1000)
    column2_width = int((220 * screen_width) / 2800)
    column3_width = int((120 * screen_width) / 1500)
    column4_width = int((120 * screen_width) / 1500)
    column5_width = int((120 * screen_width) / 1500)
    column6_width = int((120 * screen_width) /250)

    # Create the table and set the column widths
    # self.table = tk.Treeview(root)
    self.table.column("#1", anchor="c", minwidth=column1_width, width=column1_width)
    self.table.column("#2", anchor="w", minwidth=column2_width, width=column2_width)
    self.table.column("#3", anchor="c", minwidth=column3_width, width=column3_width)
    self.table.column("#4", anchor="c", minwidth=column4_width, width=column4_width)
    self.table.column("#5", anchor="c", minwidth=column5_width, width=column5_width)
    self.table.column("#6", anchor="w", minwidth=column6_width, width=column6_width)

    self.table.heading('sno', text='Sno')
    self.table.heading('name', text='Name')
    self.table.heading('ttl', text='TTL')
    self.table.heading('class_', text='Class')
    self.table.heading('type_', text='Type')
    self.table.heading('address', text='Address')

    content_list.extend(content_list)
    print(content_list)
    # content_list.extend(content_list)
    print('len(content_list)',len(content_list))
    for i in range(1, len(content_list)):
        content = content_list[i].split()
        name = content[0]
        ttl = content[1]
        class_ = content[2]
        type_ = content[3]
        address = content[4]
        self.table.insert('', 'end', values=(i,name, ttl, class_, type_, address))

    self.table.grid(row=0, column=0, sticky='nsew')

    self.table.bind('<Motion>', 'break')


# def render_dns_information(self, results_db):
#     content_list = results_db['dns']['result']
#
#     self.dns_frame = customtkinter.CTkFrame(
#         self.tabview.tab("DNS"), corner_radius=0, fg_color="transparent"
#     )
#     # root.home_frame.grid_columnconfigure(0, weight=1)
#     self.dns_frame.grid_columnconfigure(1, weight=1)
#     self.dns_frame.grid_rowconfigure((0), weight=0)
#     self.dns_frame.grid_rowconfigure((1, 2), weight=2)
#
#     self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.dns_frame, width=1400,
#                                                                     height=900,
#                                                                     corner_radius=0)
#     self.scrollable_label_button_frame.grid(row=1, column=2, padx=(1, 30), pady=(20, 10), sticky="nsew")
#     heading = customtkinter.CTkLabel(self.dns_frame, text="Hello world", compound="left", padx=5, anchor="w",
#                                    font=customtkinter.CTkFont(size=15))
#     heading.grid(row=0, column=0, pady=(10, 10), sticky="w")
#     self.dns_frame.grid()
#     for i in range(len(content_list)):
#         content = f"{content_list[i]}"
#         self.scrollable_label_button_frame.add_item(content)
#

def render_portscan_results(self, results_db):
    content_list = results_db['port']['result']
    print("content_list: ", content_list)

    self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.tabview.tab("Ports"), width=1400,
                                                                    height=900,
                                                                    corner_radius=0)
    self.scrollable_label_button_frame.grid(row=0, column=2, padx=(1, 30), pady=(20, 10), sticky="nsew")
    for i in range(len(content_list)):
        content = f"{content_list[i]}"
        self.scrollable_label_button_frame.add_ports_item(content)


def render_external_urls(self, results_db):
    if 'external_urls' in results_db and 'result' in results_db['external_urls']:
        content_list = results_db['external_urls']['result']
        print("content_list: ", content_list)

        for i in range(1, 10):
            content_list.append(f"")

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.tabview.tab("External urls"),
                                                                        width=1400,
                                                                        height=900,
                                                                        corner_radius=0)
        self.scrollable_label_button_frame.grid(row=0, column=2, padx=(1, 30), pady=(20, 10), sticky="nsew")
        for i in range(len(content_list)):
            content = f"{content_list[i]}"
            self.scrollable_label_button_frame.add_links_item(content)



def render_internal_urls(self, results_db):
    if 'internal_urls' in results_db and 'result' in results_db['internal_urls']:
        content_list = results_db['internal_urls']['result']
        print("content_list: ", content_list)

        for i in range(1, 10):
            content_list.append(f"")

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.tabview.tab("Internal urls"),
                                                                        width=1400,
                                                                        height=900,
                                                                        corner_radius=0)
        self.scrollable_label_button_frame.grid(row=0, column=2, padx=(1, 30), pady=(20, 10), sticky="nsew")
        for i in range(len(content_list)):
            content = f"{content_list[i]}"
            self.scrollable_label_button_frame.add_links_item(content)



def render_image_urls(self, results_db):
    if 'image_urls' in results_db and 'result' in results_db['image_urls']:
        content_list = results_db['image_urls']['result']
        print("content_list: ", content_list)

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self.tabview.tab("Images"), width=1400,
                                                                        height=900,
                                                                        corner_radius=0)
        self.scrollable_label_button_frame.grid(row=0, column=2, padx=(1, 30), pady=(20, 10), sticky="nsew")
        for i in range(len(content_list)):
            content = f"{content_list[i]}"
            self.scrollable_label_button_frame.add_image(content, i)

