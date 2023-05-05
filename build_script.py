import PyInstaller.__main__

PyInstaller.__main__.run([
    'web-hunter.py',     # The main Python script file of your GUI project
    '--onefile',          # Package everything into a single executable
    '--windowed',         # Launch the GUI without showing a console window
    '--icon=UI/images/logo.ico',
    '--additional-hooks-dir=.',
    '--add-data=UI/images/bg.png;UI/images/scan_light.png;',
    # '--add-data=UI/images/export_dark.png;UI/images/'

])
