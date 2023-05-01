import ipaddress
import sys
from tkinter import messagebox

import tldextract
import socket
import asyncio



def initialize_scanner(root,target, results_db):
    try:
        if target.startswith(('http', 'https')) is False:
            print(f'{R}[-] {C}Protocol Missing, Include {W}http:// {C}or{W} https:// \n')
            sys.exit(1)
        else:
            pass

        if target.endswith('/') is True:
            target = target[:-1]
        else:
            pass

        print(target)
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
