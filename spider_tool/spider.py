#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 21:23
# @Author  : CoLoDoo
# @Site    : 
# @File    : spider.py
# @Software: PyCharm

import urllib
from bs4 import BeautifulSoup

class spider:

    def __init__(self, main_url):
        self.main_url = main_url

    def start(self):
        pass

    def stop(self):
        pass

    def set_url_pool(self, pool):
        pass

    def spider_url_pool(self, url):
        tag_a_results = BeautifulSoup(urllib.urlopen(url).read(), 'html5lib').find_all('a')
