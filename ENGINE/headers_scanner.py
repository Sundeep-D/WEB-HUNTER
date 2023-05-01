import requests
requests.packages.urllib3.disable_warnings()

def headers(url, results_db):
    headers_results = {}
    result = {}
    print(f'\n[!] Headers:\n')
    try:
        rqst = requests.get(url, verify=False, timeout=10)
        for key, val in rqst.headers.items():
            # print(f'{key}: {val}')
            result[key] = val
    except Exception as e:
        print(f'\n[-] Exception: {e}\n')

    headers_results.update({'is_success': True})
    headers_results.update({'result': result})
    results_db['headers'] = headers_results
