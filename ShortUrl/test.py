# -*- coding: utf-8 -*-
# @Author: xiaobuyao
# @Date:   2017-02-04 15:50:54
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2017-05-22 00:59:27

long_url = 'https://mp.weixin.qq.com/s?__biz=MzI3ODE3NzQ1Mw==&mid=2651660005&idx=1&sn=16b579b5f629717a342161773d55f381&chksm=f0a34d27c7d4c4312ac77d9c0cee7de6f1011883b1a127b559cf74aca42730b76f3c95caf4ef&scene=21&key=dcbc515947c3a2680f21ecb850573305a4440de89495d1018b1db843c68a29116967318762117e20ec23160e18e0ff16cfb62ba4683426225ac32d8330e6394d14e3b395f750d70a36d6b5bc31eaf7bc&ascene=0&uin=NjY2MTc4ODU%3D&devicetype=iMac+MacBook9%2C1+OSX+OSX+10.12.3+build(16D32)&version=12010310&nettype=WIFI&fontScale=100&pass_ticket=X3Ag29omYiSDsykQd0HQMDY3vv5UuhO9BkeHkpiGIlM%3D'

print(long_url[8:24])
# print(long_url.split('&chksm')[0]


if 'mp.weixin.qq.com' in long_url:
    url = long_url.split('&chksm')[0]
else:
    url = long_url

print(url)



last_output = getLink(type,service,url)

if ('http' in last_output):
    print(last_output, end='')
else:
    print('Error: '+ last_output, end='')
