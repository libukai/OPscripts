# -*- coding: utf-8 -*-
# @Author: xiaobuyao
# @Date:   2016-09-20 15:55:16
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2016-11-11 22:54:21

import requests
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import os
import shutil   

def cliplist(roomid):
    originallist = 'http://playback.ks.zb.mi.com/record/live/' + str(roomid) + '/hls/' + str(roomid) + '.m3u8'
    listfile = requests.get(originallist)
    finallist = []
    for link in listfile.text.split('\n'):
        if link[0:3] == roomid[8:11]:
            finallist.append('http://playback.ks.zb.mi.com/record/live/' + str(roomid) + '/hls/' + link)
    return finallist

def download(filelink):
    clipcontent = requests.get(filelink)
    filename = os.path.join(roomid, filelink.split('/')[-1])
    with open(filename, 'ab') as clip:
        clip.write(clipcontent.content)
        # print('已获取文件 ' + filename)

def connect(roomid):
    print('正在合并视频文件，请耐心等待……')
    cmd = r'cat %s/*.ts > %s.ts' %(roomid, roomid)
    os.system( cmd )

if __name__ == '__main__':
    roomid = input('请输入房间号：')
    if os.path.isdir(roomid):
        pass
    else:
        os.mkdir(roomid)
    print('正在下载视频片段，请耐心等待……')
    pool = Pool(8)
    pool.map(download, cliplist(roomid))
    connect(roomid)
    print('正在删除临时文件，请耐心等待……')
    shutil.rmtree('%s' %(roomid))
