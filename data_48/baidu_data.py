#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/14 23:24
# @Author  : CoLoDoo
# @Site    : 
# @File    : baidu_data.py
# @Software: PyCharm

import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from bs4 import BeautifulSoup
import re

def get_result_sum(url):
    '''
    返回百度搜索的数量
    # https://www.baidu.com/s?wd=鞠婧祎
    :param url: url字符串
    :return: result: 结果数字
    '''
    res = urllib2.urlopen(url).read()
    soup = BeautifulSoup(res, 'html5lib')
    div = soup.find(attrs={'class': 'nums'})
    pattern = re.compile('约([\s\S]*?)个', re.I | re.M | re.S)
    str1 = str(div)
    result = str(pattern.search(str1).group(1)).replace(',', '')
    return result

def get_birthday(url=''):
    '''
    取得成员的生日
    # http://baike.baidu.com/item/黄彤扬
    :param url:
    :return: birthday: 生日字符串
    '''
    birthday = ''
    res = urllib2.urlopen(url).read()
    soup = BeautifulSoup(res, 'html5lib')
    dd = soup.find_all(attrs={'class': 'basicInfo-item value'})
    for item in dd:
        try:
            if u'年' in item.string:
                birthday = item.string.replace('\n', '').replace('\r', '').replace('\n\n', '')
                return birthday
        except:
            return birthday

# !!未完成
# https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=黄婷婷
# 搜索引擎弹出信息收集
def get_search_query(url):
    res = urllib2.urlopen(url).read().decode('gbk').encode('utf-8')
    return res

# if __name__ == '__main__':
#     print get_search_query('https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=曾艳芬'),

