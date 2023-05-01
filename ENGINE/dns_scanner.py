#!/usr/bin/env python3

import dnslib


def dns_scan(domain, results_db):
    dns_results = {}
    results = []
    types = ['A', 'AAAA', 'ANY', 'CAA', 'CNAME', 'MX', 'NS', 'TXT']
    full_ans = []
    for Type in types:
        q = dnslib.DNSRecord.question(domain, Type)
        pkt = q.send('8.8.8.8', 53, tcp='UDP')
        ans = dnslib.DNSRecord.parse(pkt)
        ans = str(ans)
        ans = ans.split('\n')
        full_ans.extend(ans)
    full_ans = set(full_ans)
    dns_found = []
    for entry in full_ans:
        if entry.startswith(';') is False:
            dns_found.append(entry)
        else:
            pass
    if len(dns_found) != 0:
        for entry in dns_found:
            # print(f'ENTRY: {entry}')
            results.append(str(entry))
            pass
    else:
        # print(f'{R}[-] {C}DNS Records Not Found!{W}')
        pass
    dmarc_target = f'_dmarc.{domain}'
    q = dnslib.DNSRecord.question(dmarc_target, 'TXT')
    pkt = q.send('8.8.8.8', 53, tcp='UDP')
    dmarc_ans = dnslib.DNSRecord.parse(pkt)
    dmarc_ans = str(dmarc_ans)
    dmarc_ans = dmarc_ans.split('\n')
    dmarc_found = []
    for entry in dmarc_ans:
        if entry.startswith('_dmarc') is True:
            dmarc_found.append(entry)
        else:
            pass
    if len(dmarc_found) != 0:
        for entry in dmarc_found:
            # print(f'ENTRY: {entry}')
            results.append(str(entry))
    else:
        # print(f'\n{R}[-] {C}DMARC Record Not Found!{W}')
        pass
    dns_results.update({"is_success": True})
    dns_results.update({"result": results})
    results_db["dns"] = dns_results
