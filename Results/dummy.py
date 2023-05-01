import json
import os

from fpdf import FPDF

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
    pdf.cell(50, 10, "Value", border=1)
    pdf.ln()

    # add table data
    for item in json_results['dns']['result']:
        item_list = item.split()
        pdf.cell(45, 10, item_list[3], border=1)
        pdf.cell(45, 10, item_list[1], border=1)
        pdf.multi_cell(50, 10, " ".join(item_list[4:]), border=1)
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

def dummy():
    json_str = '{"hostname": "sundeepdayalan.in", "domain": "sundeepdayalan.in", "ip": "185.230.63.186", "whois": {"is_success": true, "result": {"asn_registry": "ripencc", "asn": "58182", "asn_cidr": "185.230.63.0/24", "asn_country_code": "IL", "asn_date": "2017-11-06", "asn_description": "WIX_COM  IL", "query": "185.230.63.186", "cidr": "185.230.63.0/24", "name": "wix_com_inc", "handle": "AF14171-RIPE", "range": "185.230.63.0 - 185.230.63.255", "country": "US", "address": "Namal Tel Aviv 40 6350671 Tel Aviv ISRAEL", "created": "2018-06-14T11:45:30Z", "updated": "2018-06-14T11:45:30Z"}}, "headers": {"is_success": true, "result": {"Date": "Wed, 19 Apr 2023 06:15:45 GMT", "Content-Type": "text/html; charset=UTF-8", "Connection": "keep-alive", "link": "<https://static.parastorage.com/>; rel=preconnect; crossorigin;,<https://static.parastorage.com/>; rel=preconnect;,<https://static.wixstatic.com/>; rel=preconnect; crossorigin;,<https://static.wixstatic.com/>; rel=preconnect;,<https://siteassets.parastorage.com>; rel=preconnect; crossorigin;,", "x-wix-request-id": "1681884944.8091388170050128763", "set-cookie": "hs=-1193858803; Max-Age=-1; Expires=Wed, 19 Apr 2023 06:15:43 GMT; Path=/; Domain=www.sundeepdayalan.in; HTTPOnly, svSession=43681ff3cbc9c3f52c66915ddeb12f1746a61a244f1ad41407a70f5148b96bf238a2ed58f8d36aca093e0512f8eeb3951e60994d53964e647acf431e4f798bcdabd187ad805964a0c80e7621a6cd51ad5224eda0b5774a4e9b8744cb3038455d5f143327e133a710d8f2fa79b4af440918738b971a6a6c64fa5173ed8b7d42cb58050b77830931ee1b6ec04e69b8b719; Max-Age=63158399; Expires=Sat, 19 Apr 2025 06:15:43 GMT; Path=/; Domain=www.sundeepdayalan.in; Secure; HTTPOnly; SameSite=None, XSRF-TOKEN=1681884944|qhqtGPMXX_E_; Path=/; Domain=www.sundeepdayalan.in; Secure; SameSite=None, ssr-caching=cache#desc=none; Max-Age=20; Expires=Wed, 19 Apr 2023 06:16:04 GMT, TS01e85bed=01286b42afc2377279303bb10dd7874cd967b1022eb501d1ccdd197cadde10e4fe19199ad0d33889b91a19be859f13d544ea71a3aa; Path=/; SameSite=none; Secure, TS011cb07b=01286b42afc2377279303bb10dd7874cd967b1022eb501d1ccdd197cadde10e4fe19199ad0d33889b91a19be859f13d544ea71a3aa; path=/; domain=www.sundeepdayalan.in; SameSite=none; Secure", "vary": "Accept-Encoding", "cache-control": "no-cache", "content-language": "en", "strict-transport-security": "max-age=3600", "content-encoding": "gzip", "Age": "0", "Server-Timing": "cache;desc=none", "X-Seen-By": "9WD8GAcpJgs/Ng1WkD2i0h9slopJdhD+WySraMrpIY8=,sHU62EDOGnH2FBkJkG/Wx8EeXWsWdHrhlvbxtlynkVj9PNa9L8L9ArVPOtPklR89,m0j2EEknGIVUW/liY8BLLk1Uxi5aVwrmRyfWZ8T7SgAMbwluI1yUDJty9McxOlfY,2d58ifebGbosy5xc+FRalgfYRzF9GV5a4/8exImsokabLgSgqeTFQkwo61ownKd39/NSIdxwP0sqmyNo1Wgnkg==,2UNV7KOq4oGjA5+PKsX47FlYZdviiK1o6bY5MLS8FR4fbJaKSXYQ/lskq2jK6SGP,osV03DUdKaEVOGwoQFgPYus8W5UIU3hETi6p84yfPhM=,sQ19iEk473qMiaixh4sATkK06J7PNFn0fl+D539rqEU=,znxyTGNb715cyF9N4jtLDNvrUN8uv0IdVKJKSDRkhvzMJHuSd4nHhUN54A+lY0Kt,sQ19iEk473qMiaixh4sATkK06J7PNFn0fl+D539rqEU=,LoUK8/saGAmOxZWtpubo2hvBqlnVU7mrYpfk5pOMJybqhGIU1LU7FwII0eB59FKN5RXfLzlIxIvEQfBcVP9qGg==,sQ19iEk473qMiaixh4sATtUJhtCSt3yrx5aL5RPbx0g=,sQ19iEk473qMiaixh4sATk4mlTyDrqUq0xTnrJJrgfg=,/a5ccLSK1HEmwPNg/x6OupxKpAuO9RJddEfmEDgRsuEPDTNbAUOPESfcxDHzRkNvXo8tZ4uwU9lx9tbaIQY3Xw==", "Accept-Ranges": "bytes", "X-Content-Type-Options": "nosniff", "Transfer-Encoding": "chunked"}},{"dns":{"is_success":true,"result":["sundeepdayalan.in. 3600 IN TXT "D6909315"","sundeepdayalan.in. 3600 IN MX 10 smtp.secureserver.net.","sundeepdayalan.in. 21600 IN NS ns11.wixdns.net.","sundeepdayalan.in. 3600 IN A 185.230.63.171","sundeepdayalan.in. 21600 IN NS ns10.wixdns.net.","sundeepdayalan.in. 3600 IN SOA ns10.wixdns.net. support.wix.com. 2019081916 10800 3600 604800 3600","sundeepdayalan.in. 3600 IN MX 20 mailstore1.secureserver.net.","sundeepdayalan.in. 1800 IN SOA ns10.wixdns.net. support.wix.com. 2019081916 10800 3600 604800 3600","sundeepdayalan.in. 3600 IN TXT "v=spf1 include:secureserver.net -all"","sundeepdayalan.in. 3600 IN A 185.230.63.107","sundeepdayalan.in. 3600 IN A 185.230.63.186","sundeepdayalan.in. 3600 IN TXT "D6909315"","sundeepdayalan.in. 3600 IN MX 10 smtp.secureserver.net.","sundeepdayalan.in. 21600 IN NS ns11.wixdns.net.","sundeepdayalan.in. 3600 IN A 185.230.63.171","sundeepdayalan.in. 21600 IN NS ns10.wixdns.net.","sundeepdayalan.in. 3600 IN SOA ns10.wixdns.net. support.wix.com. 2019081916 10800 3600 604800 3600","sundeepdayalan.in. 3600 IN MX 20 mailstore1.secureserver.net.","sundeepdayalan.in. 1800 IN SOA ns10.wixdns.net. support.wix.com. 2019081916 10800 3600 604800 3600","sundeepdayalan.in. 3600 IN TXT "v=spf1 include:secureserver.net -all"","sundeepdayalan.in. 3600 IN A 185.230.63.107","sundeepdayalan.in. 3600 IN A 185.230.63.186"]}}'
    json_results = json.loads(json_str)

    pdf = FPDF()
    write_who_is_information(pdf, json_results)
    write_headers_information(pdf, json_results)
    write_dns_information(pdf, json_results)

    if not os.path.exists('Results'):
        os.makedirs('Results')
    pdf.output('Results/test.pdf', 'F')
    with open('Results/output.txt', 'w') as file:
        json.dump(json_results, file)


dummy()


