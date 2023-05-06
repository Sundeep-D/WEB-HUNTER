#!/usr/bin/env python3
"""
File: engine.py
Modified by: Sundeep Dayalan
Reference: https://github.com/thewhiteh4t/FinalRecon
Website: www.sundeepdayalan.in
Github: https://github.com/Sundeep-D/WEB-HUNTER
Date: April 22, 2023

Description: This is a helper class for all functionalities"""
import asyncio
import os
import ssl
import socket
import bs4
import requests
import tldextract
import ipwhois
import dnslib


sslp = 443
from UI.ProgressHandler import update_progress

requests.packages.urllib3.disable_warnings()
counter = 0

port_scan_results = {}
requests.packages.urllib3.disable_warnings()

USER_AGENT = {'User-Agent': 'WEB-HUNTER'}

external_urls = {}
internal_urls = {}
image_urls = {}


def headers(url, results_db):
    headers_results = {}
    result = {}
    try:
        rqst = requests.get(url, verify=False, timeout=10)
        for key, val in rqst.headers.items():
            result[key] = val
    except Exception as e:
        print(f'Exception: {e}\n')

    headers_results.update({'is_success': True})
    headers_results.update({'result': result})
    results_db['headers'] = headers_results




async def consumer(queue, ip, result, self):
    global counter
    while True:
        port = await queue.get()
        await sock_conn(ip, port, result)
        queue.task_done()
        counter += 1
        update_progress(self, f"Scanning ports {counter}/1000", 0.6)


async def run(ip, result, threads, self):
    queue = asyncio.Queue(maxsize=threads)

    distrib = asyncio.create_task(insert(queue))
    workers = [asyncio.create_task(consumer(queue, ip, result, self)) for _ in range(threads)]

    await asyncio.gather(distrib)
    await queue.join()
    for worker in workers:
        worker.cancel()


def port_scanner(ip, results_db, self):
    global counter
    counter = 0
    threads = 50
    global port_scan_results
    result = []
    result = []

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run(ip, result, threads, self))
    loop.close()
    ps_output(results_db, result)


async def sock_conn(ip, port, result):
    try:
        connector = asyncio.open_connection(ip, port)
        await asyncio.wait_for(connector, 1)
        result.append(str(port))
        return True
    except TimeoutError:
        return False
    except Exception:
        pass


def ps_output(results_db, result):
    for i in range(len(result)):
        result[i] = f"Port {result[i]} is open"
    port_scan_results.update({"is_success": True})
    port_scan_results.update({"result": result})
    results_db['port'] = port_scan_results


def sll_certificate(hostname, results_db):
    global sslp
    ssl_results = {}
    result = {}
    pair = {}
    pt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pt.settimeout(5)

    try:
        pt.connect((hostname, sslp))
        pt.close()

        ctx = ssl.create_default_context()
        sock = socket.socket()
        sock.settimeout(5)
        s = ctx.wrap_socket(sock, server_hostname=hostname)

        try:
            s.connect((hostname, sslp))
            info = s.getpeercert()
        except Exception:
            info = ssl.get_server_certificate((hostname, sslp))
            f = open(f"{hostname}.pem", "w")
            f.write(info)
            f.close()
            cert_dict = ssl._ssl._test_decode_cert(f"{hostname}.pem")
            info = cert_dict
            os.remove(f"{hostname}.pem")

        def unpack(v, pair):
            convert = False
            for item in v:
                if isinstance(item, tuple):
                    for subitem in item:
                        if isinstance(subitem, tuple):
                            for elem in subitem:
                                if isinstance(elem, tuple):
                                    unpack(elem)
                                else:
                                    convert = True
                            if convert is True:
                                pair.update(dict([subitem]))
                        else:
                            pass
                else:
                    result[k] = item

        for k, v in info.items():
            if isinstance(v, tuple):
                unpack(v, pair)
                for k, v in pair.items():
                    result[k] = v
                pair.clear()
            else:
                result[k] = v

    except Exception:
        pt.close()

    if result == {}:
        result = {"No records found": "SSL records for this url is unavailable"}

    ssl_results.update({"is_success": True})
    ssl_results.update({"result": result})
    results_db["ssl"] = ssl_results


def extract_internal_links(target_url, results_db):
    global total, int_total
    int_total = []

    try:
        response = requests.get(target_url, headers=USER_AGENT, verify=False, timeout=10)
    except Exception as e:
        return

    if response.status_code == 200:
        page_content = response.content
        soup = bs4.BeautifulSoup(page_content, 'lxml')
        ext = tldextract.extract(target_url)
        domain = ext.registered_domain

        links = soup.find_all('a')
        for link in links:
            url = link.get('href')
            if url is not None:
                if domain in url:
                    int_total.append(url)

        int_total = set(int_total)
        internal_urls_list = list(int_total)
        save_internal_urls(results_db, internal_urls_list)


def extract_external_links(target_url, results_db):
    global external_urls
    external_urls_set = set()

    try:
        response = requests.get(target_url, headers=USER_AGENT, verify=False, timeout=10)
    except Exception as e:
        return

    if response.status_code == 200:
        page_content = response.content
        soup = bs4.BeautifulSoup(page_content, 'lxml')

        ext = tldextract.extract(target_url)
        domain = ext.registered_domain

        links = soup.find_all('a')
        for link in links:
            url = link.get('href')
            if url is not None:
                if domain not in url and url.startswith('http'):
                    external_urls_set.add(url)

        external_urls_list = list(external_urls_set)
        save_external_urls(results_db, external_urls_list)


def extract_image_urls(target_url, results_db):
    global image_urls
    image_urls_set = set()

    try:
        response = requests.get(target_url, headers=USER_AGENT, verify=False, timeout=10)
    except Exception as e:
        return

    if response.status_code == 200:
        page_content = response.content
        soup = bs4.BeautifulSoup(page_content, 'lxml')

        image_tags = soup.find_all('img')
        for image in image_tags:
            url = image.get('src')
            if url is not None and len(url) > 1:
                image_urls_set.add(filter_url(target_url, url))

        image_urls_list = list(image_urls_set)
        save_image_urls(results_db, image_urls_list)


def filter_url(target_url, url):
    if url.startswith('/') and not url.startswith('//'):
        return target_url + url
    elif url.startswith('//'):
        return url.replace('//', 'http://')
    elif url.find('//') == -1 and url.find('../') == -1 and url.find('./') == -1 and url.find(
            'http://') == -1 and url.find('https://') == -1:
        return f'{target_url}/{url}'
    elif url.find('http://') == -1 and url.find('https://') == -1:
        ret_url = url.replace('//', 'http://')
        ret_url = url.replace('../', f'{target_url}/')
        ret_url = url.replace('./', f'{target_url}/')
        return ret_url
    else:
        return url


def save_external_urls(results_db, results_list):
    external_urls.update({"is_success": True})
    external_urls.update({"result": results_list})
    results_db['external_urls'] = external_urls


def save_internal_urls(results_db, results_list):
    internal_urls.update({"is_success": True})
    internal_urls.update({"result": results_list})
    results_db['internal_urls'] = internal_urls


def save_image_urls(results_db, results_list):
    image_urls.update({"is_success": True})
    image_urls.update({"result": results_list})
    results_db['image_urls'] = image_urls

async def insert(queue):
    port_list = [
        1,
        3,
        4,
        6,
        7,
        9,
        13,
        17,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        30,
        32,
        33,
        37,
        42,
        43,
        49,
        53,
        70,
        79,
        80,
        81,
        82,
        83,
        84,
        85,
        88,
        89,
        90,
        99,
        100,
        106,
        109,
        110,
        111,
        113,
        119,
        125,
        135,
        139,
        143,
        144,
        146,
        161,
        163,
        179,
        199,
        211,
        212,
        222,
        254,
        255,
        256,
        259,
        264,
        280,
        301,
        306,
        311,
        340,
        366,
        389,
        406,
        407,
        416,
        417,
        425,
        427,
        443,
        444,
        445,
        458,
        464,
        465,
        481,
        497,
        500,
        512,
        513,
        514,
        515,
        524,
        541,
        543,
        544,
        545,
        548,
        554,
        555,
        563,
        587,
        593,
        616,
        617,
        625,
        631,
        636,
        646,
        648,
        666,
        667,
        668,
        683,
        687,
        691,
        700,
        705,
        711,
        714,
        720,
        722,
        726,
        749,
        765,
        777,
        783,
        787,
        800,
        801,
        808,
        843,
        873,
        880,
        888,
        898,
        900,
        901,
        902,
        903,
        911,
        912,
        981,
        987,
        990,
        992,
        993,
        995,
        999,
        1000,
        1001,
        1002,
        1007,
        1009,
        1010,
        1011,
        1021,
        1022,
        1023,
        1024,
        1025,
        1026,
        1027,
        1028,
        1029,
        1030,
        1031,
        1032,
        1033,
        1034,
        1035,
        1036,
        1037,
        1038,
        1039,
        1040,
        1041,
        1042,
        1043,
        1044,
        1045,
        1046,
        1047,
        1048,
        1049,
        1050,
        1051,
        1052,
        1053,
        1054,
        1055,
        1056,
        1057,
        1058,
        1059,
        1060,
        1061,
        1062,
        1063,
        1064,
        1065,
        1066,
        1067,
        1068,
        1069,
        1070,
        1071,
        1072,
        1073,
        1074,
        1075,
        1076,
        1077,
        1078,
        1079,
        1080,
        1081,
        1082,
        1083,
        1084,
        1085,
        1086,
        1087,
        1088,
        1089,
        1090,
        1091,
        1092,
        1093,
        1094,
        1095,
        1096,
        1097,
        1098,
        1099,
        1100,
        1102,
        1104,
        1105,
        1106,
        1107,
        1108,
        1110,
        1111,
        1112,
        1113,
        1114,
        1117,
        1119,
        1121,
        1122,
        1123,
        1124,
        1126,
        1130,
        1131,
        1132,
        1137,
        1138,
        1141,
        1145,
        1147,
        1148,
        1149,
        1151,
        1152,
        1154,
        1163,
        1164,
        1165,
        1166,
        1169,
        1174,
        1175,
        1183,
        1185,
        1186,
        1187,
        1192,
        1198,
        1199,
        1201,
        1213,
        1216,
        1217,
        1218,
        1233,
        1234,
        1236,
        1244,
        1247,
        1248,
        1259,
        1271,
        1272,
        1277,
        1287,
        1296,
        1300,
        1301,
        1309,
        1310,
        1311,
        1322,
        1328,
        1334,
        1352,
        1417,
        1433,
        1434,
        1443,
        1455,
        1461,
        1494,
        1500,
        1501,
        1503,
        1521,
        1524,
        1533,
        1556,
        1580,
        1583,
        1594,
        1600,
        1641,
        1658,
        1666,
        1687,
        1688,
        1700,
        1717,
        1718,
        1719,
        1720,
        1721,
        1723,
        1755,
        1761,
        1782,
        1783,
        1801,
        1805,
        1812,
        1839,
        1840,
        1862,
        1863,
        1864,
        1875,
        1900,
        1914,
        1935,
        1947,
        1971,
        1972,
        1974,
        1984,
        1998,
        1999,
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008,
        2009,
        2010,
        2013,
        2020,
        2021,
        2022,
        2030,
        2033,
        2034,
        2035,
        2038,
        2040,
        2041,
        2042,
        2043,
        2045,
        2046,
        2047,
        2048,
        2049,
        2065,
        2068,
        2099,
        2100,
        2103,
        2105,
        2106,
        2107,
        2111,
        2119,
        2121,
        2126,
        2135,
        2144,
        2160,
        2161,
        2170,
        2179,
        2190,
        2191,
        2196,
        2200,
        2222,
        2251,
        2260,
        2288,
        2301,
        2323,
        2366,
        2381,
        2382,
        2383,
        2393,
        2394,
        2399,
        2401,
        2492,
        2500,
        2522,
        2525,
        2557,
        2601,
        2602,
        2604,
        2605,
        2607,
        2608,
        2638,
        2701,
        2702,
        2710,
        2717,
        2718,
        2725,
        2800,
        2809,
        2811,
        2869,
        2875,
        2909,
        2910,
        2920,
        2967,
        2968,
        2998,
        3000,
        3001,
        3003,
        3005,
        3006,
        3007,
        3011,
        3013,
        3017,
        3030,
        3031,
        3052,
        3071,
        3077,
        3128,
        3168,
        3211,
        3221,
        3260,
        3261,
        3268,
        3269,
        3283,
        3300,
        3301,
        3306,
        3322,
        3323,
        3324,
        3325,
        3333,
        3351,
        3367,
        3369,
        3370,
        3371,
        3372,
        3389,
        3390,
        3404,
        3476,
        3493,
        3517,
        3527,
        3546,
        3551,
        3580,
        3659,
        3689,
        3690,
        3703,
        3737,
        3766,
        3784,
        3800,
        3801,
        3809,
        3814,
        3826,
        3827,
        3828,
        3851,
        3869,
        3871,
        3878,
        3880,
        3889,
        3905,
        3914,
        3918,
        3920,
        3945,
        3971,
        3986,
        3995,
        3998,
        4000,
        4001,
        4002,
        4003,
        4004,
        4005,
        4006,
        4045,
        4111,
        4125,
        4126,
        4129,
        4224,
        4242,
        4279,
        4321,
        4343,
        4443,
        4444,
        4445,
        4446,
        4449,
        4550,
        4567,
        4662,
        4848,
        4899,
        4900,
        4998,
        5000,
        5001,
        5002,
        5003,
        5004,
        5009,
        5030,
        5033,
        5050,
        5051,
        5054,
        5060,
        5061,
        5080,
        5087,
        5100,
        5101,
        5102,
        5120,
        5190,
        5200,
        5214,
        5221,
        5222,
        5225,
        5226,
        5269,
        5280,
        5298,
        5357,
        5405,
        5414,
        5431,
        5432,
        5440,
        5500,
        5510,
        5544,
        5550,
        5555,
        5560,
        5566,
        5631,
        5633,
        5666,
        5678,
        5679,
        5718,
        5730,
        5800,
        5801,
        5802,
        5810,
        5811,
        5815,
        5822,
        5825,
        5850,
        5859,
        5862,
        5877,
        5900,
        5901,
        5902,
        5903,
        5904,
        5906,
        5907,
        5910,
        5911,
        5915,
        5922,
        5925,
        5950,
        5952,
        5959,
        5960,
        5961,
        5962,
        5963,
        5987,
        5988,
        5989,
        5998,
        5999,
        6000,
        6001,
        6002,
        6003,
        6004,
        6005,
        6006,
        6007,
        6009,
        6025,
        6059,
        6100,
        6101,
        6106,
        6112,
        6123,
        6129,
        6156,
        6346,
        6389,
        6502,
        6510,
        6543,
        6547,
        6565,
        6566,
        6567,
        6580,
        6646,
        6666,
        6667,
        6668,
        6669,
        6689,
        6692,
        6699,
        6779,
        6788,
        6789,
        6792,
        6839,
        6881,
        6901,
        6969,
        7000,
        7001,
        7002,
        7004,
        7007,
        7019,
        7025,
        7070,
        7100,
        7103,
        7106,
        7200,
        7201,
        7402,
        7435,
        7443,
        7496,
        7512,
        7625,
        7627,
        7676,
        7741,
        7777,
        7778,
        7800,
        7911,
        7920,
        7921,
        7937,
        7938,
        7999,
        8000,
        8001,
        8002,
        8007,
        8008,
        8009,
        8010,
        8011,
        8021,
        8022,
        8031,
        8042,
        8045,
        8080,
        8081,
        8082,
        8083,
        8084,
        8085,
        8086,
        8087,
        8088,
        8089,
        8090,
        8093,
        8099,
        8100,
        8180,
        8181,
        8192,
        8193,
        8194,
        8200,
        8222,
        8254,
        8290,
        8291,
        8292,
        8300,
        8333,
        8383,
        8400,
        8402,
        8443,
        8500,
        8600,
        8649,
        8651,
        8652,
        8654,
        8701,
        8800,
        8873,
        8888,
        8899,
        8994,
        9000,
        9001,
        9002,
        9003,
        9009,
        9010,
        9011,
        9040,
        9050,
        9071,
        9080,
        9081,
        9090,
        9091,
        9099,
        9100,
        9101,
        9102,
        9103,
        9110,
        9111,
        9200,
        9207,
        9220,
        9290,
        9415,
        9418,
        9485,
        9500,
        9502,
        9503,
        9535,
        9575,
        9593,
        9594,
        9595,
        9618,
        9666,
        9876,
        9877,
        9878,
        9898,
        9900,
        9917,
        9929,
        9943,
        9944,
        9968,
        9998,
        9999,
        10000,
        10001,
        10002,
        10003,
        10004,
        10009,
        10010,
        10012,
        10024,
        10025,
        10082,
        10180,
        10215,
        10243,
        10566,
        10616,
        10617,
        10621,
        10626,
        10628,
        10629,
        10778,
        11110,
        11111,
        11967,
        12000,
        12174,
        12265,
        12345,
        13456,
        13722,
        13782,
        13783,
        14000,
        14238,
        14441,
        14442,
        15000,
        15002,
        15003,
        15004,
        15660,
        15742,
        16000,
        16001,
        16012,
        16016,
        16018,
        16080,
        16113,
        16992,
        16993,
        17877,
        17988,
        18040,
        18101,
        18988,
        19101,
        19283,
        19315,
        19350,
        19780,
        19801,
        19842,
        20000,
        20005,
        20031,
        20221,
        20222,
        20828,
        21571,
        22939,
        23502,
        24444,
        24800,
        25734,
        25735,
        26214,
        27000,
        27352,
        27353,
        27355,
        27356,
        27715,
        28201,
        30000,
        30718,
        30951,
        31038,
        31337,
        32768,
        32769,
        32770,
        32771,
        32772,
        32773,
        32774,
        32775,
        32776,
        32777,
        32778,
        32779,
        32780,
        32781,
        32782,
        32783,
        32784,
        32785,
        33354,
        33899,
        34571,
        34572,
        34573,
        35500,
        38292,
        40193,
        40911,
        41511,
        42510,
        44176,
        44442,
        44443,
        44501,
        45100,
        48080,
        49152,
        49153,
        49154,
        49155,
        49156,
        49157,
        49158,
        49159,
        49160,
        49161,
        49163,
        49165,
        49167,
        49175,
        49176,
        49400,
        49999,
        50000,
        50001,
        50002,
        50003,
        50006,
        50300,
        50389,
        50500,
        50636,
        50800,
        51103,
        51493,
        52673,
        52822,
        52848,
        52869,
        54045,
        54328,
        55055,
        55056,
        55555,
        55600,
        56737,
        56738,
        57294,
        57797,
        58080,
        60020,
        60443,
        61532,
        61900,
        62078,
        63331,
        64623,
        64680,
        65000,
        65129,
        65389,
    ]
    for port in port_list:
        await queue.put(port)

def whois_lookup(ip_addr, results_db):
    whois_results = {}
    result = {}
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

                                    result[key] = temp_val
                                else:
                                    temp_val = ', '.join(value)

                                    result[key] = temp_val
                            else:
                                pass
                else:
                    temp_val = val.replace(',', ' ').replace('\r', ' ').replace('\n', ' ')

                    result[key] = temp_val
            else:
                pass
    except Exception as e:
        print(f'[-] Error: {e}')

    whois_results.update({'is_success': True})
    whois_results.update({'result': result})

    results_db['whois'] = whois_results


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
            results.append(str(entry))
            pass
    else:
        print(f'DNS Records Not Found!')
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
            results.append(str(entry))
    else:
        print(f'DMARC Record Not Found!')
        pass
    dns_results.update({"is_success": True})
    dns_results.update({"result": results})
    results_db["dns"] = dns_results
