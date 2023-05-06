"""
File: initializer.py
Modified by: Sundeep Dayalan
Reference: https://github.com/thewhiteh4t/FinalRecon
Website: www.sundeepdayalan.in
Github: https://github.com/Sundeep-D/WEB-HUNTER
Date: April 25, 2023

Description: This code initializes a web scanner by extracting the domain and hostname from a given target URL,
and attempts to obtain the IP address of the hostname. If it fails to get the IP address, it displays an error
message."""
import ipaddress
import sys
from tkinter import messagebox
import tldextract
import socket



def initialize_scanner(root,target, results_db):
    try:
        if target.startswith(('http', 'https')) is False:
            sys.exit(1)
        else:
            pass

        if target.endswith('/') is True:
            target = target[:-1]
        else:
            pass

        ext = tldextract.extract(target)
        domain = ext.registered_domain
        hostname = '.'.join(part for part in ext if part)
        results_db['hostname'] = str(hostname)
        results_db['domain'] = str(domain)

        try:
            ipaddress.ip_address(hostname)
            type_ip = True
            ip = hostname
        except Exception:
            try:
                ip = socket.gethostbyname(hostname)
                print(f'IP Address : {str(ip)}')
                results_db['ip'] = str(ip)
            except Exception as e:
                print(f'\nUnable to Get IP : {str(e)}')
                messagebox.showinfo(title="Invalid Url", message="The url you entered is invalid")
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
                # sys.exit(1)


    except KeyboardInterrupt:
        print(f'Keyboard Interrupt.\n')
        sys.exit(130)
