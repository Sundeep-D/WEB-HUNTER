"""
File: scanner.py
Author: Sundeep Dayalan
Website: www.sundeepdayalan.in
Github: https://github.com/Sundeep-D/WEB-HUNTER
Date: April 21, 2023

Description: This code defines a function called "perform_full_scan" that performs a full security scan on a given
website using various techniques such as whois lookup, SSL certificate gathering, port scanning, and link crawling,
among others, and updates the results on the GUI."""
import json
import time

from ENGINE.engine import whois_lookup, headers, sll_certificate, dns_scan, port_scanner, extract_external_links, \
    extract_internal_links, extract_image_urls
from ENGINE.render_results import render_who_is_information, render_headers_information, render_ssl_information, \
    render_dns_information, render_portscan_results, render_image_urls, render_external_urls, render_internal_urls

from UI.ProgressHandler import update_progress

isScanningInProgress = True


def perform_full_scan(root, results_db, url):
    json_obj = json.loads(json.dumps(results_db))

    if 'ip' in results_db:

        if isScanningInProgress:
            update_progress(root, f"looking who-is information for {results_db['ip']}", 0.1)
            whois_lookup(results_db['ip'], results_db)
            json_obj = json.loads(json.dumps(results_db))
            render_who_is_information(root, results_db)

        if isScanningInProgress:
            headers(url, results_db)
            json_obj = json.loads(json.dumps(results_db))
            render_headers_information(root, results_db)

        if isScanningInProgress:
            update_progress(root, f"Gathering SSL Certificate information for {json_obj['ip']}", 0.3)
            sll_certificate(results_db['hostname'], results_db)
            json_obj = json.loads(json.dumps(results_db))
            render_ssl_information(root, results_db)

        if isScanningInProgress:
            update_progress(root, f"Pulling the DNS records for {results_db['ip']}", 0.4)
            dns_scan(results_db['domain'], results_db)
            json_obj = json.loads(json.dumps(results_db))
            render_dns_information(root, results_db)

        if isScanningInProgress:
            update_progress(root, f"Scanning ports in {json_obj['whois']['result']['cidr']}", 0.5)
            port_scanner(results_db['ip'], results_db, root)
            json_obj = json.loads(json.dumps(results_db))
            render_portscan_results(root, results_db)

        if isScanningInProgress:
            update_progress(root, f"Crawling links in {json_obj['hostname']}", 0.8)
            extract_external_links(url, results_db)

        if isScanningInProgress:
            extract_internal_links(url, results_db)

        if isScanningInProgress:
            extract_image_urls(url, results_db)
            json_obj = json.loads(json.dumps(results_db))

        if isScanningInProgress:
            render_image_urls(root, results_db)

        if isScanningInProgress:
            update_progress(root, f"Rendering images..", 0.9)
            render_external_urls(root, results_db)

        if isScanningInProgress:
            render_internal_urls(root, results_db)

        if isScanningInProgress:
            update_progress(root, f"Finishing..", 2)

        if isScanningInProgress:
            print("FINAL JSON: ", json.dumps(results_db).replace("'", "\""))
            json_obj = json.loads(json.dumps(results_db))
            time.sleep(1)
            root.url_input.grid_remove()
            root.main_button_1.grid_remove()
            root.progressbar_1.grid_remove()
            root.progress_status.grid_remove()
            root.tabview.grid()
            root.url_info.configure(text=f'Showing results for {url}', text_color="gray")
            root.url_info.update()
            root.url_info.grid()
            root.home_frame.bg_image_label.grid_remove()
            root.new_scan_button.grid()
            root.export_button.grid()
        else:
            # scan was aborted
            print("Scan aborted.")
