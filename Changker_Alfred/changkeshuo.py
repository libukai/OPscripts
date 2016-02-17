#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2015-07-19 13:26:46
# @Last Modified by:   anchen
# @Last Modified time: 2015-08-08 09:57:40

from pync import Notifier
import requests
# import os
import sys
import time
import re
from pprint import pprint


reload (sys)
sys.setdefaultencoding('utf-8')

def newat():
	url = 'https://release2.changker.com/api/user/message/at?'
	params = dict(ckuid = 10022769, v=1.6,pagesize=10,version=1.6)
	header = {'token':'829cf1d8c08d6923df30fbb571c7ed7c'}
	success = True
	while success:
		try:
			r = requests.post(url, params, headers = header)
			success = False
		except:
			success = True
			time.sleep(60)
	r.raise_for_status()
	newat = r.json()
	return newat['data']

def newcomment():
	url = 'https://release2.changker.com/api/user/message/comment?'
	params = dict(ckuid = 10022769, v=1.6,pagesize=10,version=1.6)
	header = {'token':'829cf1d8c08d6923df30fbb571c7ed7c'}
	success = True
	while success:
		try:
			r = requests.post(url, params, headers = header)
			success = False
		except:
			success = True
			time.sleep(60)
	r.raise_for_status()
	newcomment = r.json()
	return newcomment['data']

def showfeed():
	newfeed = [at for at in reversed(newat())]
	newfeed.extend([comment for comment in reversed(newcomment())])
	showfeed = []
	for feed in newfeed:
		if (int(feed['create_time']) > int(allfeed[-1]['create_time'])):
			showfeed.append(feed)
	try:
		allfeed.append(showfeed[0])
	except:
		pass
	return showfeed

def notify(showfeed):
	for feed in showfeed:
		content = re.sub(r'<.*?>','',feed['content'],0)
		try:
			weibo = '原帖：' + re.sub(r'<.*?>','',feed['weibo']['content'],0)
		except:
			weibo = ''
		if feed['userinfo']['ext_info']['special_description'] == '':
			description = ''
		else:
			description = '   ' + '🏁' + feed['userinfo']['ext_info']['special_description']
		title = feed['userinfo']['nickname'] + '    ' + '⚠️' +'注意！' + description
		try:
			contentImage = feed['images'][0]
		except:
			contentImage = ''
		appicon = feed['userinfo']['ext_info']['avatar']
		Notifier.notify(weibo,title=title,subtitle=content,sound='default',appIcon = appicon,contentImage = contentImage)
		time.sleep(6)

if __name__ == '__main__':
	# os.system('pkill python')
	# pprint(newat())
	# pprint(newcomment())
	# starttime = int(time.mktime(datetime.datetime.now().timetuple()))
	allfeed = [{'create_time':0}]
	while True:
		notify(showfeed())
		time.sleep(60)
