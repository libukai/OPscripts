#!/usr/bin/python
#-*- coding:utf-8 -*-

from workflow import Workflow, ICON_WEB, web
import sys
import requests
# from pprint import pprint

reload (sys)
sys.setdefaultencoding('utf-8')

def usersearch(keyword):
	url = 'https://release2.changker.com/api/search/users/1?'
	params = dict(ckuid=10038452, v=1.6, nickname = keyword, pagesize = 20, version=1.6)
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
			membershipname = ''
		wf.add_item(user['nickname'], 
					'UID : '+ user['uid'] + '    性别 : '+ gendername + '    行业 : ' + user['ext_info']['profession'] + '    备注 : ' + user['ext_info']['special_description'],
					arg=membershipname,
					valid=True,
					icon= 'user.png')	
	else:
		wf.add_item('抱歉，没有找到符合条件的用户','请重新输入关键词',arg='',valid=True,icon= 'mem.png')
		wf.send_feedback()
	return user['uid']

def usermembership(useruid):
	url = 'https://release2.changker.com/api/user/'+str(useruid)+'/memberships?'
	params = dict(ckuid=10038452, v=1.6)
	header = {'token':'0f8e3c49ac7823e8c89f7e87a324686d'}
	r = requests.post(url, params, headers = header)
	r.raise_for_status()
	memberships = r.json()
	return memberships
	
def main(wf):
	keyword = wf.args[0]
	useruid = usersearch(keyword)
	memberships = usermembership(useruid)
	if not memberships['data'] == []:
		keyword = {'SP':1,'万豪':1,'洲际':1,'凯悦':1,'丽思':1,'希尔':1,'费尔':1,'香格':1,
					'东航':2,'全日':2,'凤凰':2,'南航':2,'厦航':2,'国泰':2,'新航':2,'汉莎':2,'海航':2,'美联':2,'英航':2,'荷法':2,'达美':2,'阿航':2,'美航':2}	
		for membership in memberships['data']:
			if keyword[str(membership['level'][0:2])] == 1: 
				jumpurl = 'https://cms.changker.com/index.php?MembershipHotel%5Bid%5D=&MembershipHotel%5Bmtype%5D=&MembershipHotel%5Bcard_no%5D=&MembershipHotel%5Buid%5D='+str(useruid)+'&MembershipHotel%5Blevel%5D=&MembershipHotel%5Bpoints%5D=&MembershipHotel%5Bstays%5D=&MembershipHotel%5Bnights%5D=&MembershipHotel%5Bupdate_time%5D=&MembershipHotel_page=1&r=membership%2Fhotel'
			else:
				jumpurl = 'https://cms.changker.com/index.php?MembershipAirline%5Bid%5D=&MembershipAirline%5Bmtype%5D=&MembershipAirline%5Bcard_no%5D=&MembershipAirline%5Buid%5D='+str(useruid)+'&MembershipAirline%5Blevel%5D=&MembershipAirline%5Bmileages%5D=&MembershipAirline%5Bstages%5D=&MembershipAirline%5Bupgrade_mileages%5D=&MembershipAirline%5Bupdate_time%5D=&MembershipAirline_page=1&r=membership%2Fairline'	
			wf.add_item(membership['level'], 
				'',
				arg=jumpurl,
				valid=True,
				icon= 'mem.png')
	else:
		wf.add_item('该用户没有任何精英会籍','',arg='',valid=True,icon= 'mem.png')
	wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
