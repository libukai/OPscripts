#!/usr/bin/env python
# @Author: Libukai
# @Date:   2015-09-10 15:28:19
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2016-11-12 15:30:15

'''
1. 清洗微博 URL 地址，获取用户 ID 关键词。然后根据关键词类型，调用不同的开放平台接口，获取用户账号详细信息
2. 请将微博 URL 列表按照一行一个的格式保存至 url.txt 文件，不允许有空行或者非微博 URL 地址，否则会报错
3. 尝试使用多线程工具，提升网络信息获取的速度，需注意过度使用 APPKEY 可能引发的无访问权限的问题
'''


import re
import json
import sys
import requests
import random
from multiprocessing.dummy import Pool


def getkey(user_file):
    '''清理非标准化的微博地址，提取用户的 UID 或者个性化域名'''
    url_key_list = []
    listnum = 0
    with open(user_file, 'r') as url_list:
        for url in url_list:
            # 确定处理 url.txt 文件的进度，以及判断是否有错误，并标注出错位置，
            listnum += 1
            try:
                # 任意微博地址均可全部转换为标准的 weibo.com/xxxxxxx 格式
                # 1. xxx 如果为 10 位纯数字，则代表 UID
                # 2. 蓝V账号的 ID 和真实 UID 之间存在确定的转换关系，取后十位即为对应的 UID
                # 3. 除此之外的 4~32 位数字和字母的组合均可视为个性化域名，包括非 10 位的纯数字的微号或者 UC 号
                # 4. 纯数字的 UC 号除了可视为个性化域名外，也直接是对应账号的 UID
                keyword = re.search(r'\/(\d{10})|com\/(\w{4,32})|\/p\/\d{6}(\d{10})|^(\d{5,10})$', url).groups()
                url_key_list.append([key for key in keyword if key is not None][0])
            except AttributeError:
                print('第 %d 行格式有误：' % listnum, url)
        if listnum != len(url_key_list):
            unuseful = listnum - len(url_key_list)
            print('\n注意：总计发现%d个错误格式，请修正后再执行' % unuseful)
            sys.exit()
    return url_key_list

def getinfo(url_key):
    '''
    通过 APP KEY 调用开放平台的接口，针对 UID 和个性化域名获取不同的属性值
    微博开放平台接口测试地址：http://open.weibo.com/tools/apitest.php
    使用 APP KEY 的授权方式，可以绕过大多数情况下的访问频次限制
    新浪微博新加入了 IP 限制，需要使用代理服务器列表
    '''
    cookies = {'cookie':'_s_tentry=sports.sina.com.cn; Apache=5684546479023.993.1421292196940; SINAGLOBAL=5684546479023.993.1421292196940; login_sid_t=cb5d7743dab7af103e334087d3ebb9cd; ULV=1452486293137:1:1:1:5684546479023.993.1421292196940:; myuid=3862957272; SUHB=0sqwhJQB-BiWVh; wvr=6; SUB=_2AkMh9p1gdcPhrAJXm_EWy2PlaoxH-jjGieTAAX_rJkMxanB-7TxnqLfNgt9GN-NkSbyzTl85MEeZDkF1; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5dWFUjmBXWy6PCSKzVIgeW5JpX5KMt; UOR=sports.sina.com.cn,widget.weibo.com,www.google.com; JSESSIONID=01AEDDFBDF05817248AC5A84A1828CB8'}
    proxy = {'http': random.choice(proxies)}
    appkey = appkey_list[2]
    if re.match(r'\d{10}', url_key):
        params = {'source': appkey, 'uid': url_key}
        user_info = requests.get('https://api.weibo.com/2/users/show.json', params=params, proxies=proxy, cookies=cookies).json()
        try:    
            if user_info['domain'] == '':
                user_url = 'http://weibo.com/' + str(url_key)
            else:
                user_url = 'http://weibo.com/' + user_info['domain']
            clean_info = [url_key, user_url, user_info['screen_name'], user_info['id']]            
        except:
            clean_info = [url_key, 'http://weibo.com/%s' % url_key, '注意：账号异常', '注意：账号异常']
    else:
        params = {'source': appkey, 'domain': url_key}
        user_info = requests.get('https://api.weibo.com/2/users/domain_show.json', params=params, proxies=proxy, cookies=cookies).json() 
        user_url = 'http://weibo.com/' + str(url_key)
        try:
            clean_info = [url_key, user_url, user_info['screen_name'], user_info['id']]
        except:
            clean_info = [url_key, 'http://weibo.com/%s' % url_key, '注意：账号异常', '注意：账号异常']
    return clean_info


def result_file(clean_info, user_list):
    '''
    将多线程获取的网络信息结果从列表格式转化为字典格式，
    然后与初始 UID/ 昵称列表匹配，保持原有的顺序便于后续处理
    '''
    user_detail = {}    
    for user_info_clean in clean_info:
        url_key, user_url, user_nickname, user_uid = user_info_clean
        user_detail[url_key] = str(user_uid), user_nickname, user_url
    with open('result.txt', encoding = 'utf-8', mode = 'w+') as result:
        for url_key in user_list:
            line_content = '\t'.join(user_detail[url_key])
            print(line_content)
            print(line_content, file = result)

if __name__ == '__main__':
    with open('perference.json', 'r') as perference:
        '''将涉及到个人信息的配置文件独立出来，避免个人信息泄露'''
        perference_items = json.load(perference)
        # 配置文件中有四个可用 APPKEY，可根据需要选用 0~8
        appkey_list = perference_items['appkeys']
    with open('../Proxy_Fetch/proxy.json', 'r') as proxy_file:
        proxies = list(dict(json.load(proxy_file)).items())


    # 请将 URL 列表按照一行一个的格式保存至 url.txt 文件，不允许有空行或者非微博地址格式
    user_list = getkey('url.txt')
    # 使用多线程，加快涉及到网络接口的信息获取速度
    pool = Pool(8)
    # # 对原始用户表进行排重处理，减少需要网络查询的次数
    clean_info = pool.map(getinfo, set(user_list))
    pool.close()
    pool.join()
    # 处理多线程获取的信息，进行输出
    result_file(clean_info, user_list)
