#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 22:53
# @Author  : CoLoDoo
# @Site    : 
# @File    : tool.py
# @Software: PyCharm

import urllib2
import urllib
from bs4 import BeautifulSoup
import json

def find_all(url, tag, attr={}):
    '''
    Beautifulsoup工具方法
    :param url:
    :param tag:
    :param attr:
    :return:
    '''
    return BeautifulSoup(urllib.urlopen(url).read(), 'html5lib').find_all(tag, attrs=attr)

def some2json(data):
    return json.dumps(data)