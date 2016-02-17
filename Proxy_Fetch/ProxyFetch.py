#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Libukai
# @Date:   2016-01-27 11:00:41
# @Last Modified by:   Libukai
# @Last Modified time: 2016-02-17 15:14:35


import json
import random
import requests
from lxml import html
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


def get_proxy(url_list):
    headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
    proxies_list = []
    proxy_page = requests.get(url_list, headers=headers, proxies={}, cookies={})
    print(proxy_page.status_code)
    proxy_html = html.fromstring(proxy_page.content)
    proxy_rows = proxy_html.xpath(".//tr[@class='odd' or @class='']")
    for proxy_detail in proxy_rows:
        ip_address = proxy_detail[2].text
        ip_port = proxy_detail[3].text
        ip_type = proxy_detail[6].text.lower()
        proxies_list.append((ip_type, '{0}://{1}:{2}'.format(ip_type, ip_address, ip_port)))
    return proxies_list

def check_proxy(proxy_all, check_url):
    # 设置要验证的网址，以后可以调整到Main函数中
    check_url = 'https://www.weibo.com'
    headers = {'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
    proxies_list =[]
    ip_type, ip_address = proxy_all
    use_proxy = {ip_type: ip_address}
    try:
        proxy_api = requests.get(check_url, proxies=use_proxy, timeout=1)
        if proxy_api.status_code == 200 and proxy_api.elapsed.total_seconds() < 1:
            proxies_list.append((ip_type, ip_address, proxy_api.elapsed.total_seconds()))
            print('难得，{0}\t此代理服务器可用!'.format(ip_address))
            return (ip_type, ip_address)
        else:
            print('妈的，{0}\t此代理服务器不可用。'.format(ip_address))
    except:
            print('妈的，{0}\t此代理服务器不可用。'.format(ip_address))
    

def convert_json(proxy_active):
    proxy_result = {}
    for proxy in proxy_active:
        if proxy: 
           proxy_result[proxy[1]] = proxy[0]
    print('共计找到{0}个可用的代理……'.format(len(proxy_result)))

    with open('proxy.json', mode='w') as proxy_json:
        proxy_json.write(json.dumps(proxy_result))


if __name__ == '__main__':
    type = {'nn':'国内高匿', 'nt':'国内普通', 'wn':'国外高匿', 'wt':'国外普通'}
    url_list = ['http://www.xicidaili.com/nn/' + str(i) for i in range(1,11)]

    pool1 = ThreadPool(3)
    proxy_list = pool1.map(get_proxy, url_list)
    proxy_all = [proxy for proxy_page in proxy_list for proxy in proxy_page]
    print('获取代理服务器共 {0} 个'.format(len(proxy_all)))

    pool2 = ThreadPool(3)
    proxy_active = pool2.map(check_proxy, proxy_all)

    convert_json(proxy_active)
