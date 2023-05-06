#File: main.spec
#Author: Sundeep Dayalan
#Website: www.sundeepdayalan.in
#Github: https://github.com/Sundeep-D/WEB-HUNTER
#Date: April 20, 2023
#
#Description:
#This code is used to create an executable file for a Python script using PyInstaller.
#It imports collect_data_files from PyInstaller.utils.hooks to collect data files required for
#the application. The Analysis object is initialized with the input script, binaries,
#and data files, and the hiddenimports, excludes, and runtime_hooks options are set.
#The pyz object is created with the PYZ method, and the exe object is created with the
#EXE method, which generates the final executable file with the given name and options.

block_cipher = None
from PyInstaller.utils.hooks import collect_data_files

gui_packages = collect_data_files('customtkinter')
a = Analysis(['web-hunter.py'],
             pathex=['C:\\Python36\\Scripts'],
             binaries=[],
             datas=[('UI/images/bg.png', 'UI/images'),
                 ('UI/images/scan_light.png', 'UI/images'),
                 ('UI/images/scan_dark.png', 'UI/images'),
                 ('UI/images/add_user_dark.png', 'UI/images'),
                 ('UI/images/add_user_light.png', 'UI/images'),
                 ('UI/images/chat_dark.png', 'UI/images'),
                 ('UI/images/chat_light.png', 'UI/images'),
                 ('UI/images/date.png', 'UI/images'),
                 ('UI/images/error.PNG', 'UI/images'),
                 ('UI/images/export_dark.png', 'UI/images'),
                 ('UI/images/export_light.png', 'UI/images'),
                 ('UI/images/home_dark.png', 'UI/images'),
                 ('UI/images/home_light.png', 'UI/images'),
                 ('UI/images/id.png', 'UI/images'),
                 ('UI/images/info.png', 'UI/images'),
                 ('UI/images/ip.png', 'UI/images'),
                 ('UI/images/link.png', 'UI/images'),
                 ('UI/images/location.png', 'UI/images'),
                 ('UI/images/logo.ico', 'UI/images'),
                 ('UI/images/name.png', 'UI/images'),
                 ('UI/images/open.png', 'UI/images'),
                 ('UI/images/port.png', 'UI/images')]+gui_packages,
             hiddenimports=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='WEB HUNTER',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
