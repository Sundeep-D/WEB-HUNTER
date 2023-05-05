from PyInstaller.utils.hooks import collect_data_files
print("CALLED")
datas = collect_data_files('customtkinter')
