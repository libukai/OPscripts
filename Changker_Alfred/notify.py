#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Libukai
# @Date:   2015-07-19 13:26:46
# @Last Modified by:   Libukai
# @Last Modified time: 2015-09-08 02:25:56

from pync import Notifier
import requests
import os
import sys
import re
import time

reload(sys)
sys.setdefaultencoding('utf-8')


def newfeed():
    url = 'https://release2.changker.com/api/recommend/feeds?'
    params = dict(ckuid='10003137', v='1.6.3', pagesize='20', version='1.6.3')
    header = {'token': 'f61f45ac2289d9caa90d932e6c5878aa'}
    success = True
    while (if success is True):
        try:
            r = requests.post(url, params, headers=header)
            newfeed = r.json()
            success = False
        except:
            time.sleep(60)
    return newfeed


def showfeed():
    try:
        showfeed = []
        for feed in newfeed()['data']:
            if (not int(feed['type']) == 4) and (int(feed['create_time']) > int(allfeed[-1]['create_time'])):
                showfeed.append(feed)
        allfeed.append(showfeed[0])
    except:
        showfeed = []
    return reversed(showfeed)



def notify(showfeed):
    try:
        for feed in showfeed:
            content = feed['content']
            retext = re.sub(ur'<.*?>', '', content, 0)
            keyword = re.compile(ur'常客说|李凯|young|水洋|协议|转让', re.M)
            if re.search(keyword, retext) == None:
                notice = ''
            else:
                notice = '    ' + '⚠️' + '注意'
            if feed['userinfo']['ext_info']['special_description'] == '':
                description = ''
            else:
                description = '    ' + '🏁' + \
                    feed['userinfo']['ext_info']['special_description']
            title = feed['userinfo']['nickname'] + notice + description
            try:
                contentImage = feed['images'][0]
            except:
                contentImage = ''
            appicon = feed['userinfo']['ext_info']['avatar']
            feedurl = 'https://cms.changker.com/index.php?r=weibo/view&id=' + str(feed['id'])
            Notifier.notify(retext, title=title, sound='default',
                            appIcon=appicon, open=feedurl, contentImage=contentImage)
            time.sleep(6)
    except:
        Notifier.notify(
            '请重新启动新内容推送', title='注意！线上数据获取不成功！', sound='default', appIcon=appicon)

if __name__ == '__main__':
    os.system('pkill python')
    allfeed = [{'create_time': 0}]
    while True:
        notify(showfeed())
        time.sleep(60)
