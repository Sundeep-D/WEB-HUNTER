#!/usr/bin/env python3

import bs4
import requests
import tldextract

requests.packages.urllib3.disable_warnings()

USER_AGENT = {'User-Agent': 'WEB-HUNTER'}

external_urls = {}
internal_urls = {}
image_urls = {}


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
        print("Internal URLs:")
        print(internal_urls_list)
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
        print("External URLs:")
        print(external_urls_list)
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
        print("Image URLs:")
        print(image_urls_list)
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
