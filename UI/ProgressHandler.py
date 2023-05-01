def update_progress(self, progress_text, progress_value):
    self.progress_status.configure(text=progress_text, text_color="gray")
    self.progress_status.update()
    self.progressbar_1.set(progress_value)