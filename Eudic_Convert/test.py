#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Libukai
# @Date:   2016-01-22 20:29:35
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2016-09-20 19:33:30


from requests import Request, Session

url = 'https://api.weibo.com/2/users/show.json' 
params = {'source':'140226478','uid':'1077127694'}

s = Session()
req = Request('GET', url=url, params=params)

prepped = s.prepare_request(req)
resp = s.send(prepped)


