# -*- coding: utf-8 -*-
# @Author: xiaobuyao
# @Date:   2016-09-20 15:55:16
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2017-05-22 00:00:37
# 需要 Chrome 插件 VideoDownloadHelper 获取对应的视频播放列表地址
# 需要 FFmpeg 命令行工具的支持，完成下载的短视频合并和格式转换部分工作

import io
import sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

import requests
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import os
import shutil

def cliplist(playlist):
    listfile = requests.get(playlist)
    clarity = playlist.split('/')[-1].split('.')[0]
    # 流畅：450；标清：850；高清：1200；超清：2000
    finallist = []
    with open('filelist.txt','w+') as f:
        for link in listfile.text.split('\n'):
            if link.endswith('ts'):
                finallist.append('http://asp.cntv.lxdns.com/asp/hls/' + clarity + '/0303000a/3/default/' + playid + '/' + link)
                print('file ./%s/' %playid + link, file = f)
                # 将文件名按照播放顺序直接存入文件，减少后续重新排序的麻烦
    return finallist

def download(finallist):
    clipcontent = requests.get(finallist)
    filename = os.path.join(playid, finallist.split('/')[-1])
    # 将文件存入对应的文件夹下，便于后续的合并操作
    with open(filename, 'ab') as clip:
        clip.write(clipcontent.content)

def connect(playid):
    print('正在合并及转换视频格式，请耐心等待……')
    cmd = r"ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy %s.mp4" % outputname
    # 使用 FFmpeg 命令行工具，自动完成下载短视频的合并及格式转换
    os.system(cmd)

if __name__ == '__main__':
    playlist = input('请输入视频播放地址：')
    outputname = input('请输入输出文件名：')
    # 需要 Chrome 插件 VideoDownloadHelper 获取对应的视频播放列表地址
    playid = playlist.split('/')[-2]
    if os.path.isdir(playid):
        pass
    else:
        os.mkdir(playid)
    print('正在下载视频片段，请耐心等待……')
    pool = Pool(8)
    pool.map(download, cliplist(playlist))
    connect(playid)
    print('正在删除临时文件，请耐心等待……')
    shutil.rmtree('%s' %(playid))
