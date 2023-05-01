import urllib
from tkinter import Label, Canvas, Frame
from tkinter.ttk import Scrollbar

from PIL import Image, ImageTk
import requests
from io import BytesIO
import ssl



def rendgrid(self):
    # Disable SSL verification
    ssl._create_default_https_context = ssl._create_unverified_context

    # Download the images and create PhotoImage objects for them
    image_links = ["https://file-examples.com/storage/feb401d325641db2fa1dfe7/2017/10/file_example_JPG_100kB.jpg",
                   "https://file-examples.com/storage/feb401d325641db2fa1dfe7/2017/10/file_example_JPG_100kB.jpg"
                   ,"https://file-examples.com/storage/feb401d325641db2fa1dfe7/2017/10/file_example_JPG_100kB.jpg",
                   "https://file-examples.com/storage/feb401d325641db2fa1dfe7/2017/10/file_example_JPG_100kB.jpg",
                   "https://file-examples.com/storage/feb401d325641db2fa1dfe7/2017/10/file_example_JPG_100kB.jpg"]
    images = []
    for link in image_links:
        with urllib.request.urlopen(link) as url:
            image = Image.open(url)
            photo = ImageTk.PhotoImage(image)
            images.append(photo)

    # Create Label widgets for each image and position them in a grid
    for i, image in enumerate(images):
        row = i // 3
        col = i % 3
        label = Label(master=self.tabview.tab("DNS"), image=image)
        # label.grid(row=row, column=col)
        label.pack()


    # self.mainloop()
