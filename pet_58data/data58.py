#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/16 10:27
# @Author  : CoLoDoo
# @Site    : 
# @File    : data58.py
# @Software: PyCharm

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
from bs4 import BeautifulSoup
import tool

def get_hour_pet_infos(url):
    '''
    获取每小时的宠物信息
    :param city: 城市简写
    :return: result[n]['data']|['title']: 结果列表
    '''
    results = []
    tds = tool.find_all(url, 'td', attr={'class', 'pd'})
    for td in tds:
        if '分钟' in td.string:
            # print td.string + ':',
            # td.string
            # td.parent.td.a.string.replace('\n', '').replace('\t', '')
            tmp = {'date': td.string,
                   'title': td.parent.td.a.string.replace('\n', '').replace('\t', ''),
                   'url': td.parent.td.a['href']}
            # print td.parent.td.a.string.replace('\n', '').replace('\t', '') + ':'
            results.append(tmp)
    return results


def get_detail_in_url(url, title='', date=''):
    '''
    取得详情页的详细信息
    1.介绍
    2.宠物图片
    # http://sh.58.com/cwzengsong/27680592060368x.shtml?psid=146124219194937492258099171&entinfo=27680592060368_0
    :param url:
    :return: results:
    '''

    soup = BeautifulSoup(urllib.urlopen(url).read(), 'html5lib')
    articles = tool.find_all(url, 'article', attr={'class', 'description_con'})
    # print articles
    art_string = ''
    for art in articles:
        soup_art = BeautifulSoup(str(art), 'html5lib')
        ps = soup_art.find_all('p')
        for p in ps:
            art_string += str(p.string)
    # art = {'article':art_string.replace('<p>', '').replace('</p>', '')}
    art = {'article': art_string}
    div = soup.find('div', attrs={'class', 'descriptionImg'})
    try:
        img = {'img': div.li.a.img['lazy_src']}
    except:
        img = {'img': ''}

    results = dict(img.items()+art.items()+{'title': title}.items()+{'date': date}.items())

    return results


# for result in get_hour_pet_infos('http://sh.58.com/cwzengsong/'):
#     print result['date'],
#     print result['title'],
#     print result['url']
#     print get_detail_in_url(result['url'])
