import ipwhois


def whois_lookup(ip_addr, results_db):
    whois_results = {}
    result={}
    print('[!] Whois Lookup:\n')
    try:
        lookup = ipwhois.IPWhois(ip_addr)
        results = lookup.lookup_whois()

        for key, val in results.items():
            if val is not None:
                if isinstance(val, list):
                    for item in val:
                        for key, value in item.items():
                            if value is not None:
                                if not isinstance(value, list):
                                    temp_val = value.replace(',', ' ').replace('\r', ' ').replace('\n', ' ')
                                    #print(f'[++] {key}: {temp_val}')
                                    result[key] = temp_val
                                else:
                                    temp_val = ', '.join(value)
                                    #print(f'[+++] {key}: {temp_val}')
                                    result[key] = temp_val
                            else:
                                pass
                else:
                    temp_val = val.replace(',', ' ').replace('\r', ' ').replace('\n', ' ')
                    #print(f'[++++] {key}: {temp_val}')
                    result[key] = temp_val
            else:
                pass
    except Exception as e:
        print(f'[-] Error: {e}')

    whois_results.update({'is_success': True})
    whois_results.update({'result': result})

    results_db['whois'] = whois_results
