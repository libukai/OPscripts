# -*- coding: utf-8 -*-
# @Author: xiaobuyao
# @Date:   2016-11-19 18:27:50
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2016-12-13 14:08:54

import os
import requests
import glob
import codecs
import hashlib
import time
from multiprocessing.dummy import Pool

def get_online_info(mailNo):
   
    api = 'http://route.showapi.com/64-19'
    # 对密匙进行MD5加密，避免密匙失窃，加密逻辑见：https://www.showapi.com/api/lookPoint/64/19
    showapi_sign = hashlib.md5(('comautonu%sshowapi_appid276148623aafb0653415a88bc7434b07a8e23' %(mailNo)).encode(encoding='utf-8')).hexdigest()
    params = {'showapi_appid': '27614', 'showapi_sign': showapi_sign, 'com': 'auto', 'nu': mailNo}
    headers = {}

    try:
        online_info = requests.get(api, params = params, headers = headers, timeout = 10).json()
        # 根据查询到的数据，为文件中的快递单号标注不同的状态
        if online_info['showapi_res_body']['status'] == 4:
            key_info = [mailNo, '已送达***', online_info['showapi_res_body']['expSpellName'],online_info['showapi_res_body']['data'][1]['time']]
        elif online_info['showapi_res_body']['status'] == 1:
            key_info = [mailNo, '未入库!!!']
        else:
            key_info = [mailNo, '配送中...']
    except:
        key_info = [mailNo, '没查到???']
    # 每个线程结束后增加0.2秒暂停，减少查询服务器方面的压力
    time.sleep(0.2)
    print('\t'.join(key_info))
    return key_info

def refresh_single_file(filename):
    # 对单个文件的数据进行更新
    with codecs.open(filename, 'r', 'utf-8') as file_content:
    # 写入中文字符到文件中，需要解决编码问题
        old_online_info = []
        new_online = []
        for record_info in file_content:
            try:
                # 二次运行获取首次失败单号信息时，应修改条件值为 ('已送达***', '配送中...')
                if record_info.split()[1] in ('已送达***'):
                    old_online_info.append(record_info.split())
                else:
                    new_online.append(record_info.split()[0])
            except:
                new_online.append(record_info.split()[0])
    # 设置为同时并发4个线程，避免线程过多导致的访问失败
    pool = Pool(4)
    new_online_info = pool.map(get_online_info, new_online)
    # 将读取和写回的操作放入同一个函数中，便于更好的循环使用
    with codecs.open(filename, 'w', 'utf-8') as file_content:
        for online_info in old_online_info + new_online_info:
            print('\t'.join(online_info), file = file_content)

def refresh_all_file(file_list):
    # 对所有的文件进行数据更新
    for filename in file_list:
        refresh_single_file(filename)

def cal_all_date(file_list):
    # 统计每日固定时刻的总到达数，直接生成 Markdown 的表格文件，节约工作量
    print('\n|','日期','|','发货数','|','送达数','|', '送达比', '|')
    print('|','---','|','---','|','---','|', '---','|') 
    all_count, over_count = 0, 0
    for filename in file_list:
        with codecs.open(filename, 'r', 'utf-8') as file_content:
            count_all, count_over = 0, 0
            for line_content in file_content:
                count_all += 1
                if line_content.split()[1] == '已送达***':
                    unix_time = time.mktime(time.strptime(' '.join(line_content.split()[2:4]), '%Y-%m-%d %H:%M:%S'))
                    # 增加对于送达时间的判断，便于和日报其他内容的统计时间保持一致
                    check_time_down = time.mktime(time.strptime('2016-12-02 18:00:00', '%Y-%m-%d %H:%M:%S'))
                    check_time_up = time.mktime(time.strptime('2016-12-10 18:00:00', '%Y-%m-%d %H:%M:%S'))
                    if unix_time < check_time_down:
                        count_over += 1
        print('|',os.path.splitext(filename)[0].split('/')[-1],'|',count_all,'|', count_over,'|', format(count_over/count_all, '.2%'), '|')
        all_count += count_all
        over_count += count_over
    print('|', '总计', '|', all_count, '|', over_count,'|', format(over_count/all_count, '.2%'), '|')
    
                    
if __name__ == '__main__': 
    # 原始的快递单号文件需要进行正则表达式处理：将.*(\d{12}).* 替换为 \1
    file_list = glob.glob('./test/*.txt')
    # 更新快递的最新线上数据
    refresh_all_file(file_list) 
    # 分析线下数据，生成各种报表
    # cal_all_date(file_list)
