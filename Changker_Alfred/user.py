#!/usr/bin/python
#-*- coding:utf-8 -*-

from workflow import Workflow, ICON_WEB, web
import sys
import requests
import re
import time
import datetime


reload (sys)
sys.setdefaultencoding('utf-8')

def usersearch(keyword):
	url = 'https://release2.changker.com/api/search/users/1?'
	params = dict(ckuid='10038452', v='1.6.3', nickname = keyword, pagesize = '20', version = '1.6.3')
	header = {'token':'0f8e3c49ac7823e8c89f7e87a324686d'}
	r = requests.post(url, params, headers = header)
	r.raise_for_status()
	users = r.json()
	if not users['data'] == []:
		user = users['data'][0]
		useruid = users['data'][0]['uid']
		gender = {'1':'男','2':'女', '3': '同'}
		gendername = gender[user['ext_info']['gender']]
		if not user['icons'] == []:
			membershipname = '/'.join([icon['level'] for icon in user['icons']])
		else:
			membershipname = '该用户没有任何精英会籍'
		url = 'https://cms.changker.com/index.php?r=user/view&id=' + str(useruid)
		if user['ext_info']['special_description'] == '' : 
			special_description = '待分类'
		else:
			special_description = user['ext_info']['special_description']
		wf.add_item(user['nickname'] + '    UID : '+ user['uid'] + '    备注 : ' + special_description,
					'精英会籍：' + membershipname,
					arg=url,
					valid=True,
					icon= 'user.png')
	else:
		wf.add_item('抱歉，没有找到符合条件的用户','请重新输入关键词',arg='',valid=True,icon= 'mem.png')
		wf.send_feedback()
	return user['uid']

def userfeed(useruid):
	url = 'https://release2.changker.com/api/user/'+str(useruid)+'/feeds?'
	params = dict(ckuid=10038452, v=1.6, pagesize = 20, version=1.6)
	header = {'token':'0f8e3c49ac7823e8c89f7e87a324686d'}
	r = requests.post(url, params, headers = header)
	r.raise_for_status()
	userfeed = r.json()
	return userfeed

def TimeToString(timestamp):
    t_tuple = time.localtime(timestamp)
    dt = datetime.datetime(*t_tuple[:6])
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def main(wf):
	keyword = wf.args[0]
	useruid = usersearch(keyword)
	try:
		userfeeds = userfeed(useruid)
		if not userfeeds['data'] == []:
			for feed in userfeeds['data']:
				if not feed['type'] == '4':
					url = 'https://cms.changker.com/index.php?r=weibo/view&id=' + str(feed['id'])
					time = TimeToString(float(feed['create_time']))
					content = feed['content']
					retext = re.sub(r'<.*?>','',content,0)
					wf.add_item(retext,
						'发布时间：' + time + '          评论数：' + feed['comment_count'].ljust(10) + '        点赞数：' +  feed['praise_count'] ,
						arg = url,
						valid = True,
						icon = 'mem.png')
			url = 'https://cms.changker.com/index.php?Weibo%5Bid%5D=&Weibo%5Buid%5D=' + str(feed['uid']) + '&Weibo%5Btype%5D=&Weibo%5Bcontent%5D=&Weibo%5Bcomment_count%5D=&Weibo%5Bpraise_count%5D=&Weibo%5Bstatus%5D=&Weibo%5Bcreate_time%5D=&Weibo_page=1&Weibo_sort=id.desc&r=weibo%2Findex'
			wf.add_item('查看用户所有发言内容',
			'',
			arg=url,
			valid=True,
			icon= 'add.png')
		else:
			wf.add_item('该用户没有任何发言，或者删除了所有发言','',arg='',valid=True,icon= 'mem.png')
	except:
		wf.add_item('该用户发言不对所有用户开放','',arg='',valid=True,icon= 'mem.png')
	wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
