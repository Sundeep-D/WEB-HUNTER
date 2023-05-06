"""
File: export.py
Author: Sundeep Dayalan
Website: www.sundeepdayalan.in
Github: https://github.com/Sundeep-D/WEB-HUNTER
Date: May 2, 2023

Description: This code generates a PDF report of various information about a given website, including WHOIS and DNS
information. It uses the fpdf library to create the PDF document and Tkinter to prompt the user to select a directory
to save the report."""
import time
from datetime import datetime
from tkinter import Tk, filedialog

from fpdf import FPDF

max_chars_per_line = 80  # Maximum characters per line


def add_scan_header(pdf, json_results):
    # Write hostname, domain, and IP
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 10.0)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='Hostname: ' + json_results['hostname'], border=0)
    pdf.ln(h=8)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='Domain: ' + json_results['domain'], border=0)
    pdf.ln(h=8)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='IP: ' + json_results['ip'], border=0)
    pdf.ln(h=20)


def add_cover_page_header(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 30.0)
    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=85.0, align='C', w=0, txt='WEB HUNTER RESULTS', border=0)
    pdf.ln(h=80)
    # Write hostname, domain, and IP
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 15.0)
    pdf.cell(ln=0, h=10.0, align='C', w=0, txt='Hostname: ' + json_results['hostname'], border=0)
    pdf.ln(h=10)
    pdf.cell(ln=0, h=10.0, align='C', w=0, txt='Domain: ' + json_results['domain'], border=0)
    pdf.ln(h=10)
    pdf.cell(ln=0, h=10.0, align='C', w=0, txt='IP: ' + json_results['ip'], border=0)
    pdf.ln(h=10)
    pdf.cell(ln=0, h=10.0, align='C', w=0, txt='Date ' + f"{datetime.now()}", border=0)
    pdf.ln(h=40)
    pdf.set_font('Arial', '', 10.0)
    pdf.cell(ln=0, h=10.0, align='C', w=0, txt='This website scan is performed just for school educational purpose',
             border=0)


def write_who_is_information(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 16.0)

    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=15.0, align='L', w=0, txt='WHO-IS INFORMATION', border=0)
    pdf.ln(h=20)

    add_scan_header(pdf, json_results)

    # Write whois information
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='Whois Information', border=0)
    pdf.ln(h=15)
    pdf.set_font('Arial', '', 12.0)
    for key, value in json_results['whois']['result'].items():
        pdf.cell(ln=0, h=10.0, align='L', w=0, txt=key + ':', border=0)
        pdf.set_xy(80, pdf.get_y())
        pdf.cell(ln=0, h=10.0, align='L', w=0, txt=str(value), border=0)
        pdf.ln(h=8)


def write_dns_information(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 16.0)

    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=15.0, align='L', w=0, txt='DNS INFORMATION', border=0)
    pdf.ln(h=20)

    add_scan_header(pdf, json_results)
    # add table header
    pdf.cell(45, 10, "Type", border=1)
    pdf.cell(45, 10, "TTL", border=1)
    pdf.cell(100, 10, "Value", border=1)
    pdf.ln()

    # add table data
    for item in json_results['dns']['result']:
        item_list = item.split()
        pdf.cell(45, 10, item_list[3], border=1)
        pdf.cell(45, 10, item_list[1], border=1)
        pdf.cell(100, 10, " ".join(item_list[4:]), border=1)
        pdf.ln()


def write_headers_information(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 16.0)

    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=15.0, align='L', w=0, txt='HEADERS INFORMATION', border=0)
    pdf.ln(h=20)

    add_scan_header(pdf, json_results)

    # Write whois information
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='Headers Information', border=0)
    pdf.ln(h=15)
    pdf.set_font('Arial', '', 12.0)
    for key, value in json_results['headers']['result'].items():
        pdf.cell(ln=0, h=10.0, align='L', w=0, txt=key + ':', border=0)
        pdf.set_xy(80, pdf.get_y())
        pdf.cell(ln=0, h=10.0, align='L', w=0, txt=str(value), border=0)
        pdf.ln(h=8)


def write_ports_information(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 16.0)

    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=15.0, align='L', w=0, txt='PORT SCANNING RESULTS', border=0)
    pdf.ln(h=20)

    add_scan_header(pdf, json_results)

    # Write ports information
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='Ports', border=0)
    pdf.ln(h=15)
    pdf.set_font('Arial', '', 12.0)
    for value in json_results['port']['result']:
        if value != "":
            # Split value into multiple lines if it exceeds the maximum length
            lines = [value[i:i + max_chars_per_line] for i in range(0, len(value), max_chars_per_line)]

            for line in lines:
                pdf.cell(ln=0, h=10.0, align='L', w=0, txt=line, border=0)
                pdf.set_xy(80, pdf.get_y())
                pdf.ln(h=6)

            pdf.ln(h=8)


def write_external_url_information(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 16.0)

    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=15.0, align='L', w=0, txt='EXTERNAL URLS', border=0)
    pdf.ln(h=20)

    add_scan_header(pdf, json_results)

    # Write ports information
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='External Urls', border=0)
    pdf.ln(h=15)
    pdf.set_font('Arial', '', 12.0)
    for value in json_results['external_urls']['result']:
        if value != "":
            # Split value into multiple lines if it exceeds the maximum length
            lines = [value[i:i + max_chars_per_line] for i in range(0, len(value), max_chars_per_line)]

            for line in lines:
                pdf.cell(ln=0, h=10.0, align='L', w=0, txt=line, border=0)
                pdf.set_xy(80, pdf.get_y())
                pdf.ln(h=6)

            pdf.ln(h=8)


def write_internal_url_information(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 16.0)

    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=15.0, align='L', w=0, txt='INTERNAL URLS', border=0)
    pdf.ln(h=20)

    add_scan_header(pdf, json_results)

    # Write ports information
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='Internal Urls', border=0)
    pdf.ln(h=15)
    pdf.set_font('Arial', '', 12.0)
    for value in json_results['internal_urls']['result']:
        if value != "":
            # Split value into multiple lines if it exceeds the maximum length
            lines = [value[i:i + max_chars_per_line] for i in range(0, len(value), max_chars_per_line)]

            for line in lines:
                pdf.cell(ln=0, h=10.0, align='L', w=0, txt=line, border=0)
                pdf.set_xy(80, pdf.get_y())
                pdf.ln(h=6)

            pdf.ln(h=8)


def write_images_url_information(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 16.0)

    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=15.0, align='L', w=0, txt='IMAGE URLS', border=0)
    pdf.ln(h=20)

    add_scan_header(pdf, json_results)

    # Write ports information
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='Image Urls', border=0)
    pdf.ln(h=15)
    pdf.set_font('Arial', '', 12.0)
    for value in json_results['image_urls']['result']:
        if value != "":
            # Split value into multiple lines if it exceeds the maximum length
            lines = [value[i:i + max_chars_per_line] for i in range(0, len(value), max_chars_per_line)]

            for line in lines:
                pdf.cell(ln=0, h=10.0, align='L', w=0, txt=line, border=0)
                pdf.set_xy(80, pdf.get_y())
                pdf.ln(h=6)

            pdf.ln(h=8)


def write_ssl_information(pdf, json_results):
    pdf.add_page()
    pdf.set_left_margin(20)
    pdf.set_top_margin(20)
    pdf.set_xy(20, 20)
    pdf.set_font('Arial', 'B', 16.0)

    # Write title
    pdf.set_text_color(0, 128, 255)
    pdf.cell(ln=0, h=15.0, align='L', w=0, txt='SSL CERTIFICATE INFORMATION', border=0)
    pdf.ln(h=20)

    add_scan_header(pdf, json_results)

    # Write whois information
    pdf.set_font('Arial', 'B', 14.0)
    pdf.cell(ln=0, h=10.0, align='L', w=0, txt='SSL Information', border=0)
    pdf.ln(h=15)
    pdf.set_font('Arial', '', 12.0)
    for key, value in json_results['ssl']['result'].items():
        pdf.cell(ln=0, h=10.0, align='L', w=0, txt=key + ':', border=0)
        pdf.set_xy(80, pdf.get_y())
        pdf.cell(ln=0, h=10.0, align='L', w=0, txt=str(value), border=0)
        pdf.ln(h=8)


def export(json_results):
    print("Exporting results in PDF")
    pdf = FPDF()
    add_cover_page_header(pdf, json_results)
    if 'whois' in json_results and 'result' in json_results['whois']:
        write_who_is_information(pdf, json_results)
    if 'headers' in json_results and 'result' in json_results['headers']:
        write_headers_information(pdf, json_results)
    if 'dns' in json_results and 'result' in json_results['dns']:
        write_dns_information(pdf, json_results)
    if 'port' in json_results and 'result' in json_results['port']:
        write_ports_information(pdf, json_results)
    if 'external_urls' in json_results and 'result' in json_results['external_urls']:
        write_external_url_information(pdf, json_results)
    if 'internal_urls' in json_results and 'result' in json_results['internal_urls']:
        write_internal_url_information(pdf, json_results)
    if 'image_urls' in json_results and 'result' in json_results['image_urls']:
        write_images_url_information(pdf, json_results)
    if 'ssl' in json_results and 'result' in json_results['ssl']:
        write_ssl_information(pdf, json_results)

    root = Tk()
    root.withdraw()
    initial_file_name = f"{json_results['hostname']}-{int(time.time())}"
    file_path = filedialog.asksaveasfilename(
        initialfile=initial_file_name,
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )
    root.destroy()

