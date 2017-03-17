#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/13 16:57
# @Author  : CoLoDoo
# @Site    : 
# @File    : zhihu_data.py
# @Software: PyCharm

import urllib
import urllib2
import re
from bs4 import BeautifulSoup
import json

def get_question_aggree_num(id):
    '''
    获取问题的回复数量
    # https://www.zhihu.com/question/[id - 49239044]
    :param url: url地址
    :return: num: 问题回复整数
    '''
    num = 0
    for line in urllib.urlopen('https://www.zhihu.com/question/' + id).readlines():
        if 'zh-question-answer-num' in line:
            num = BeautifulSoup(line, 'html5lib').find('h3')['data-num']
    return num

def get_search_aggree_nums(key):
    '''
    搜索结果的最多赞同量结果
    # https://www.zhihu.com/search?type=content&q=[key]
    :param url: url地址
    :return: search_aggree_nums: 赞同数降序列表
    '''

    search_aggree_nums = []

    res = urllib.urlopen('https://www.zhihu.com/search?type=content&q=' + key).read()
    # print res
    bs_res = BeautifulSoup(res, 'html5lib')
    tags_a = bs_res.find_all('a')

    for tag_a in tags_a:
        if 'js-vote-count' in str(tag_a):
            pattern = re.compile('[1-9]\d*')
            str1 = str(tag_a.string)
            try:
                search_aggree_nums.append(pattern.search(str1).group(0))
            except:
                pass

    return search_aggree_nums

def get_rearch_result_num(key):
    '''
    相关搜索结果的数量
    # 'https://www.zhihu.com/r/search?q=[key]'
    :param url: url地址
    :return: num: 搜索数量整数
    '''
    res = ''
    num = 10
    url = 'https://www.zhihu.com/r/search?q=' + key
    while res == '' or str(res) != '{"paging":{"next":""},"htmls":[]}':
        try:
            res = urllib2.urlopen(url + '&offset=' + str(num)).read()
            print res
        except Exception, e:
            print '[!] 获取结果失败:{0}:{1}'.format(str(e), url)
            return 0
        num = num + 10
    return num

if __name__ == '__main__':
    print get_question_aggree_num(id='49239044')
