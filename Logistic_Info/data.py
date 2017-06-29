# -*- coding: utf-8 -*-
# @Author: xiaobuyao
# @Date:   2016-11-24 22:23:07
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2016-12-03 23:59:14

# 自动分析发货单号原始文件，生成标准格式的单号文件

import glob
import os
import re
import codecs

def data_clear(filelist, out_file):

    id = re.compile(r'\d{12}')
    recordid = []

    for data_file in file_list:
        with codecs.open(data_file, 'rb', 'GB2312') as file_content:
            for record in file_content:
                recordid.extend(id.findall(record))

    with codecs.open(out_file, 'w', 'utf-8') as file_content:
        for record in set(recordid):
            print(record, file = file_content)

if __name__ == '__main__':
    file_list = glob.glob('./test/*.dat')
    out_file = './test/1203.txt'
    data_clear(file_list, out_file)
