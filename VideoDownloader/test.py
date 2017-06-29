# -*- coding: utf-8 -*-
# @Author: xiaobuyao
# @Date:   2017-05-08 14:10:07
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2017-05-09 12:53:11

import m3u8

playlist = 'http://asp.cntv.lxdns.com/asp/hls/850/0303000a/3/default/f62392cf61bc4decab9663c9d398d384/2000.m3u8'

m3u8_obj = m3u8.load(playlist)

# playid = playlist.split('/')[-2]
# playid = playlist.split('/')[-1].split('.')[0]

m3u8_obj.is_variant

for playlist in m3u8_obj.playlists:
    playlist.uri
    playlist.stream_info.bandwidth
