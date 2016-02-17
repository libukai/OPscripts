#!/usr/bin/python
#-*- coding:utf-8 -*-

from workflow import Workflow, ICON_WEB, web
import sys
import requests
import re


reload(sys)
sys.setdefaultencoding('utf-8')


def hotelsearch(keyword):
    url = 'https://release2.changker.com/api/search/hotels/combo?'
    params = dict(ckuid='10038452', v='1.6', poi='39.984450,116.489390',
                  name=keyword, pagesize='20', version='1.6')
    header = {'token': '0f8e3c49ac7823e8c89f7e87a324686d'}
    try:
        r = requests.post(url, params, headers=header)
        r.raise_for_status()
        hotels = r.json()
        hotel = hotels['data'][0]
    except:
        wf.add_item('抱歉，没有找到符合条件的酒店', '请重新输入关键词', arg=None, valid=False, icon='hotel.png')
        wf.send_feedback()
    return hotel['uid']


def hoteldetail(hoteluid):
    url = 'https://release2.changker.com/api/hotel/' + str(hoteluid) + '?'
    params = dict(ckuid='10038452', version='1.6')
    header = {'token': '0f8e3c49ac7823e8c89f7e87a324686d'}
    try:
        r = requests.post(url, params, headers=header)
        r.raise_for_status()
        hoteldetail = r.json()
        if not hoteldetail['data'] == []:
            hotel = hoteldetail['data']
            detailurl = 'https://cms.changker.com/index.php?r=hotel/update&id=' + str(hotel['uid'])
            if hotel['scores']['share_count'] == None:
                hotel['share_count'] = '0'
            if hotel['photos'] == None:
                hotel['photos'] = '0'
            if hotel['reviews'] == None:
                hotel['reviews'] = '0'
            wf.add_item(hotel['name'],
                        '类型 : ' + hotel['category']['name'] + '    分享数 : ' + str(hotel['scores']['share_count']) + '    平均分 : ' + str(
                            hotel['scores']['score_average']) + '      展示图：' + str(len(hotel['photos'])) + '      点评数：' + str(len(hotel['reviews'])),
                        arg=detailurl,
                        valid=True,
                        icon='hotel.png')
            picurl = 'https://cms.changker.com/index.php?r=photo/create&mid=' + \
                str(hotel['uid']) + '&type=hotel'
            wf.add_item('为该酒店添加新的展示图'
                        '',
                        arg=picurl,
                        valid=True,
                        icon='add.png')
            reviewurl = 'https://cms.changker.com/index.php?r=review/create&mid=' + \
                str(hotel['uid']) + '&type=hotel'
            wf.add_item('为该酒店添加新的点评语'
                        '',
                        arg=reviewurl,
                        valid=True,
                        icon='add.png')
        else:
            wf.add_item('抱歉，没有找到符合条件的酒店', '请重新输入关键词', arg=None, valid=False, icon='hotel.png')
            wf.send_feedback()
    except:
        wf.add_item('抱歉，没有找到符合条件的酒店', '请重新输入关键词', arg=None, valid=False, icon='hotel.png')
        wf.send_feedback()


def hotelfeed(hoteluid):
    url = 'https://release2.changker.com/api/hotel/' + str(hoteluid) + '/feedlist?'
    params = dict(ckuid=10038452, v=1.6, pagesize=20, version=1.6)
    header = {'token': '0f8e3c49ac7823e8c89f7e87a324686d'}
    try:
        r = requests.post(url, params, headers=header)
        r.raise_for_status()
        hotelfeed = r.json()
    except:
        wf.add_item('没有获取到该酒店信息，请重试', '', arg='', valid=True, icon='mem.png')
        wf.send_feedback()
    return hotelfeed


def main(wf):
    keyword = wf.args[0]
    hoteluid = hotelsearch(keyword)
    try:
        hoteldetail(hoteluid)
        hotelfeeds = hotelfeed(hoteluid)
        if not hotelfeeds['data']['info'] == []:
            for feed in hotelfeeds['data']['info']:
                url = 'https://cms.changker.com/index.php?r=weibo/view&id=' + str(feed['id'])
                content = feed['content']
                retext = re.sub(r'<.*?>', '', content, 0)
                wf.add_item(retext,
                            'ID：' + feed['id'] + '        UID：' + feed['uid'] + '         图片数：' + str(
                                len(feed['images'])) + '        评论数：' + feed['comment_count'] + '        点赞数：' + feed['praise_count'],
                            arg=url,
                            valid=True,
                            icon='mem.png')
        else:
            wf.add_item('该酒店暂时还没有点评', '', arg='', valid=True, icon='mem.png')
    except:
        wf.add_item('没有获取到该酒店信息，请重试', '', arg='', valid=True, icon='mem.png')
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
