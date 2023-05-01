
import os
import ssl
import socket

sslp = 443


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
    print("SSL: ",result)
    ssl_results.update({"is_success": True})
    ssl_results.update({"result": result})
    results_db["ssl"] = ssl_results
