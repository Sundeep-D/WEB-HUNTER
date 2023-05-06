"""
File: ProgressHandler.py
Author: Sundeep Dayalan
Website: www.sundeepdayalan.in
Github: https://github.com/Sundeep-D/WEB-HUNTER
Date: April 28, 2023

Description: This code updates a GUI progress bar with a new value and status text."""
def update_progress(self, progress_text, progress_value):
    self.progress_status.configure(text=progress_text, text_color="gray")
    self.progress_status.update()
    self.progressbar_1.set(progress_value)