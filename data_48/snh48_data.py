#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/14 10:37
# @Author  : CoLoDoo
# @Site    : 
# @File    : snh48_data.py
# @Software: PyCharm

import urllib2
import re
from bs4 import BeautifulSoup
import json


def get_users(url):
    '''
    获取所有成员名
    # http://www.snh48.com/member_list.php
    :param url: url字符串
    :return: users: 成员列表
    '''
    users = []
    try:
        bs_res = BeautifulSoup(urllib2.urlopen(url).read(), 'html5lib')
        divs = bs_res.find_all('div')
        for div in divs:
            try:
                cls = div['class']
                if 'mh_w1' in cls:
                    # print div
                    pattern = re.compile('/>([\s\S]*?)</', re.I | re.M | re.S)
                    str1 = str(div)
                    user = pattern.search(str1).group(1).strip().replace(' ', '')
                    users.append(user)
            except Exception, e:
                pass
    except:
        pass
    return users


print get_users(url='http://www.snh48.com/member_list.php')