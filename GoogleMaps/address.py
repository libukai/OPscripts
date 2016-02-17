#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Libukai
# @Date:   2015-07-19 13:26:46
# @Last Modified by:   Libukai
# @Last Modified time: 2015-07-26 00:43:22


import googlemaps
import csv
import ssl

import sys
reload (sys)
sys.setdefaultencoding('utf-8')
#设置全局环境支持 UTF-8

import warnings
warnings.filterwarnings("ignore") 
#忽略 SSL 连接 Warning

import socket
import socks
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1",8964)
socket.socket = socks.socksocket
#设置代理访问 Google Maps API

def csvconvert(filename): 
	'''转化 CSV 文件,返回一个每行数据都是一个字典的列表'''
	csvlist = []
	with open(filename) as csvobject:
		csvfile = csv.DictReader(csvobject)
		for row in csvfile:
			csvlist.append(row)
	return csvlist 

def getaddress(poi):
	'''从 Google Map API 获取数据，并转化为常客数据库格式'''

	gmaps = googlemaps.Client(key='AIzaSyAoF1OIhZoyi986G_p-GhXPMrq29I-c0dg')
	#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
	#从地址查找对应的 POI
	status = False	
	while status == False :
		try:
			reverse_geocode_result = gmaps.reverse_geocode(poi)
		except Exception, e:
			print e
			status = False
		else:
			status = True
	#从 POI 查找对应的地址，如果遇到错误，则重试

	formatted_address = reverse_geocode_result[0]['formatted_address'].split(',') 
	useful_address = {	'address' : reverse_geocode_result[0]['formatted_address'][0:-5], #直接使用标准格式地址，去除国家代码
				   	'city' : formatted_address[-3].strip(),
				  	'province': formatted_address[-2][0:3].strip(),
					'country': 'us' #针对美国酒店单独赋值
					} 
	return useful_address

def newdata(filename):
	newlist = csvconvert(filename)[0:50]
	#处理文档中的哪部分数据，免费 API 每天支持2500次调用
	hotelnumber = 0
	for hotellist in newlist:
		poi = [float(poistring) for poistring in hotellist['poi'].split(',')]
		poidetial = getaddress(poi)
		hotellist['address'] = poidetial['address']
		hotellist['city'] = poidetial['city']
		hotellist['province'] = poidetial['province']
		hotellist['country'] = poidetial['country']
		hotelnumber = hotelnumber + 1
		print '已经查询第%d个酒店数据：%s' %(hotelnumber,hotellist['name_en'])
	return newlist

def newcsv(fileinput,fileoutput):
	header = ['uid','name_en','poi','country','province','city','address']
	with open(fileoutput,'w') as csvobject:
		filecsv = csv.DictWriter(csvobject,header)
		filecsv.writeheader()
		filecsv.writerows(newdata(fileinput))

if __name__ == '__main__':
	newcsv('hotel.csv','new.csv')
