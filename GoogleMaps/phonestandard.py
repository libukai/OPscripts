#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Libukai
# @Date:   2015-07-19 13:26:46
# @Last Modified by:   Libukai
# @Last Modified time: 2015-07-26 15:53:30

import csv
import string

import sys
reload (sys)
sys.setdefaultencoding('utf-8')
#设置全局环境支持 UTF-8

def csvconvert(filename): 
	'''转化 CSV 文件,返回一个每行数据都是一个字典的列表'''
	csvlist = []
	with open(filename) as csvobject:
		csvfile = csv.DictReader(csvobject)
		for row in csvfile:
			csvlist.append(row)
	return csvlist 


def newdata(filename):
	newlist = csvconvert(filename)[1:]
	hotelnumber = 0
	numbers = string.maketrans('','')
	for hotellist in newlist:
		try:
			number = str(hotellist['tel'].translate(numbers,'+()- '))
			hotellist['tel'] = '+'+number[0]+'('+number[1:4]+')'+number[4:]
		except Exception, e:
			pass
		hotelnumber = hotelnumber + 1
		print '已经修正第%d个酒店数据：%s' %(hotelnumber,hotellist['tel'])
	return newlist

def newcsv(fileinput,fileoutput):
	header = ['uid','name_en','tel']
	with open(fileoutput,'w') as csvobject:
		filecsv = csv.DictWriter(csvobject,header)
		filecsv.writeheader()
		filecsv.writerows(newdata(fileinput))

if __name__ == '__main__':
	newcsv('originalphone.csv','rightphone.csv')
