#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Libukai
# @Date:   2016-01-20 22:02:47
# @Last Modified by:   xiaobuyao
# @Last Modified time: 2016-11-19 16:19:05


from lxml import etree
from collections import defaultdict

def Parse_Dict_XML(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()
    xml_data = defaultdict(list)
    for elem in root.xpath('.//termEntry'):
        # 每个词条的内容都使用了一个名为 termEntry 的 element 进行封装
    
        en = elem.xpath('.//langSet[lang("en-US")]').pop()
        word = en.findtext('./ntig/termGrp/term') # 英文术语
        note = en.findtext('./ntig/termGrp/termNote') # 词性
        explain = en.findtext('./descripGrp/descrip') # 解释
        cn = elem.xpath('.//langSet[lang("zh-cn")]').pop()
        chn = cn.findtext('./ntig/termGrp/term') # 中文术语

        # # for subelem in elem.findall('langSet'):
        #     # 每个词条的详细解释，都分为了中英文两个部分
        #     if str(*subelem.attrib.values()) == 'en-US':
        #         word = subelem.findtext('./ntig/termGrp/term') # 英文术语
        #         note = subelem.findtext('./ntig/termGrp/termNote') # 词性
        #         explain = subelem.findtext('./descripGrp/descrip') # 解释
        #     else:
        #         chn = subelem.findtext('./ntig/termGrp/term') # 中文术语

        xml_data[word].append((note, explain, chn)) # 将重复的词条汇总到一起
    xml_data = sorted(xml_data.items(), key=lambda x : (-len(x[1]), x[0])) # 按照解释词条的数量和字母顺序排序
    return xml_data

def Convert_to_eudic(xml_data, dict_file):
    with open(dict_file, mode = 'w', encoding = 'utf-8') as f:
        for word, value in xml_data:
            if len(value) == 1:
                item_value = value[0]
                print(word, '@' ,'<I>[{0}]</I> '.format(item_value[0]), item_value[1] ,' <B>{0}</B>'.format(item_value[2]), sep = '', file = f)
                # 具体的导出文本格式，请参见 eudic_builder 中的说明
            else:    
                num = 0
                content = []
                for item_value in value:
                    num += 1
                    content.append('<B>{0}</B>. '.format(str(num)) + '<I>[{0}]</I> '.format(item_value[0]) + item_value[1] + ' <B>{0}</B>'.format(item_value[2]))
                print(word+'@'+'<BR>'.join(content), file = f)

if __name__ == '__main__':
    xml_file = 'MicrosoftTermCollection.tbx'
    Convert_to_eudic(Parse_Dict_XML(xml_file), str(xml_file[:-3] + 'txt'))
