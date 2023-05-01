import json
import time

from ENGINE.dns_scanner import dns_scan
from ENGINE.export import export
from ENGINE.headers_scanner import headers
from ENGINE.port_scanner import port_scanner
from ENGINE.render_results import render_who_is_information, render_headers_information, render_ssl_information, \
    render_dns_information, render_portscan_results, render_image_urls, render_external_urls, render_internal_urls
from ENGINE.ssl_scanner import sll_certificate
from ENGINE.web_crawler import extract_external_links, extract_image_urls, extract_internal_links
from ENGINE.whois_scanner import whois_lookup
from UI.ProgressHandler import update_progress

isScanningInProgress = True


def perform_full_scan(root, results_db, url):
    json_obj = json.loads(json.dumps(results_db))
    print(results_db)


    if 'ip' in results_db:
        print("IP received: ", results_db['ip'])
        print("DATA1: ", results_db)
        # check isScanningInProgress
        if isScanningInProgress:
            update_progress(root, f"looking who-is information for {results_db['ip']}", 0.1)
            whois_lookup(results_db['ip'], results_db)
            json_obj = json.loads(json.dumps(results_db))
            render_who_is_information(root, results_db)

        # check isScanningInProgress
        if isScanningInProgress:
            headers(url, results_db)
            json_obj = json.loads(json.dumps(results_db))
            render_headers_information(root, results_db)

        # check isScanningInProgress
        if isScanningInProgress:
            update_progress(root, f"Gathering SSL Certificate information for {json_obj['ip']}", 0.3)
            sll_certificate(results_db['hostname'], results_db)
            json_obj = json.loads(json.dumps(results_db))
            render_ssl_information(root, results_db)

        # check isScanningInProgress
        if isScanningInProgress:
            update_progress(root, f"Pulling the DNS records for {results_db['ip']}", 0.4)
            dns_scan(results_db['domain'], results_db)
            json_obj = json.loads(json.dumps(results_db))
            render_dns_information(root, results_db)

        # check isScanningInProgress
        if isScanningInProgress:
            update_progress(root, f"Scanning ports in {json_obj['whois']['result']['cidr']}", 0.5)
            port_scanner(results_db['ip'], results_db, root)
            json_obj = json.loads(json.dumps(results_db))
            render_portscan_results(root, results_db)

        # check isScanningInProgress
        if isScanningInProgress:
            extract_external_links(url, results_db)

        # check isScanningInProgress
        if isScanningInProgress:
            extract_internal_links(url, results_db)

        # check isScanningInProgress
        if isScanningInProgress:
            extract_image_urls(url, results_db)
            json_obj = json.loads(json.dumps(results_db))

        # check isScanningInProgress
        if isScanningInProgress:
            render_image_urls(root, results_db)

        # check isScanningInProgress
        if isScanningInProgress:
            render_external_urls(root, results_db)

        # check isScanningInProgress
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



