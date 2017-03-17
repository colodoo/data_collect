#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/1 21:25
# @Author  : CoLoDoo
# @Site    : 
# @File    : weibo_data.py
# @Software: PyCharm

import requests
import sys
import json
import MySQLdb
from datetime import date
import time
import datetime
import cgi
import urllib
import urllib2
import snh48_data
import types

reload(sys);
exec("sys.setdefaultencoding('utf-8')");

DB_IP = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_DATABASE = 'snh48_data'

def get(url=''):
    '''
    # 返回json loads
    :param url:
    :return:
    '''
    # return json.loads(requests.get(url=url, proxies={'http':'http://218.76.84.206:3128'}).content)
    try:
        # results = json.loads(requests.get(url=url, proxies={'http': 'http://115.231.175.68:8081'}, timeout=5).content)
        results = json.loads(requests.get(url=url, timeout=5).content)
    except:
        return ''

    return results

API = {
    'info': 'http://m.weibo.cn/container/getIndex?type=uid&value={0}',
    'content': 'http://m.weibo.cn/container/getIndex?type=uid&value={0}&containerid=107603{1}',
    'content_with_page':'http://m.weibo.cn/container/getIndex?type=uid&value={0}&containerid=107603{1}&page={2}',
    'content_in': 'http://m.weibo.cn/api/comments/show?id={0}',
    'conteng_in_with_page': 'http://m.weibo.cn/api/comments/show?id={0}&page={1}',
    'search': 'http://m.weibo.cn/container/getIndex?type=all&queryVal={0}&luicode=10000011&lfid=106003type=1&title={1}&containerid=100103type=1&q={2}',
    'forward_like_reply_num': 'http://m.weibo.cn/container/getIndex?type=uid&value={0}&containerid=107603{1}',
}

USERS = {
    'GNZ48-王盈': '6034778078',
    'SNH48-黄彤扬': '5863498042',
    'SNH48-曾艳芬': '3669076064',
    'SNH48-李钊-': '5460951688',
    'SNH48-鞠婧祎': '3669102477'
}

IP_POOL = [
    {'http': 'http://221.204.136.196:9797'},
    {'http': 'http://211.101.153.126:8080'},
    {'http': 'http://115.171.61.112:3128'},
    {'http': 'http://115.231.175.68:8081'},
]

def check_ip_proxy(pool=''):
    '''
    检测可用代理
    :param pool:
    :return:
    '''
    for ip in IP_POOL:
        try:
            res = requests.get(url='http://qq.com', proxies=ip, timeout=5)
            print str(ip) + ':' + str(res)
        except Exception, e:
            print u'[!] {0}:失败'.format(str(ip)) + ':' + str(e)
            continue

def test():
    '''
    测试
    :return:
    '''
    id = '5863498042'
    # 信息 抓关注的
    url_info = 'http://m.weibo.cn/container/getIndex?type=uid&value=' + id
    # 抓发布内容
    url_content = 'http://m.weibo.cn/container/getIndex?type=uid&value='+ id +'&containerid=107603' + id
    # 发布内容详情
    url_content_in = 'http://m.weibo.cn/api/comments/show?id=4080603349342982&page=1'
    # 抓搜索结果
    url_search = 'http://m.weibo.cn/container/getIndex?type=all&queryVal=SNH48-黄彤扬-' \
                 '&luicode=10000011&lfid=106003type=1&title=SNH48-黄彤扬-' \
                 '&containerid=100103type=1&q=SNH48-黄彤扬-'

    # send_headers = {
    #     'Host': 'm.weibo.cn',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    #     'Accept-Encoding':'gzip, deflate',
    #     'Cookie': 'SCF=Av6W3mb740biFp2YmPYGIi1dxZOi8mZcVeKDZ-dAarmWk8VF3OJXg3wWwAfaHj8QVBn3PWE1Efd24x6M0s2mh0A.; SUHB=0auRB68J0sHM_-; SSOLoginState=1488374102; ALF=1490966076; SUB=_2A251srkGDeTxGeRK61AY-CnIwjiIHXVXXMdOrDV6PUJbktBeLU7RkW2CLyrKIj_w7NM1RbzqrR5sia8JMw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW4aCby-aj4yObIrDHNvb395JpX5o2p5NHD95QESh5E1KnNSh.XWs4Dqcj_i--NiKLhiKLsi--fiK.7iKy2i--Ri-zNi-8si--Xi-iWi-iWi--4iKnfi-zp; _T_WM=4ad3b427cf2136fcdae22a9e14aaa174; M_WEIBOCN_PARAMS=luicode%3D20000174',
    #     'Connection':'keep-alive',
    #     'Upgrade-Insecure-Requests':'1'
    # }
    print url_content
    res = get(url=url_content)
    # print res.headers
    result = res
    return result

    # print json.loads(result)['userInfo']['followers_count']

def get_follower_count(id=''):
    '''
    # 取粉丝数量
    :param id:
    :return:
    '''
    url_info = 'http://m.weibo.cn/container/getIndex?type=uid&value=' + id
    count_json = get(url=url_info)
    try:
        result = [count_json['userInfo']['screen_name'], count_json['userInfo']['followers_count']]
    except Exception,e:
        print '[!] 你可能被封了!'
        return []
    return result

def get_content_with_page_list(id='', count=0):
    '''
    # 取内容列表，带page参数
    :param id:
    :param count:
    :return:
    '''
    content_with_page_lists = list()
    for i in range(1, count):
        content_with_page_list = get(url=API['content_with_page'].format(id, id, i))['cards']
        for content_with_page in content_with_page_list:
            user_id = str(id)
            content_id = content_with_page['mblog']['id']
            # print get(url=API['content_in'].format(content_id))
            created_at = content_with_page['mblog']['created_at'].replace(u'今天', str(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
            if u'分钟' in created_at:
                created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            text = str(cgi.escape(content_with_page['mblog']['text'])).replace("\'", '"')
            content_with_page_lists.append((user_id, content_id, created_at, text))
            # print content_id + ':' +created_at + ':' + text
    return content_with_page_lists

def get_content_list(id=''):
    '''
    # 取内容列表
    :param id:
    :return:
    '''
    content_lists = []
    content_list = get(url=API['content'].format(id, id))['cards']
    for content in content_list:
        user_id = str(id)
        content_id = content['mblog']['id']
        # print get(url=API['content_in'].format(content_id))
        created_at = content['mblog']['created_at'].replace(u'今天', str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
        if u'分钟' in created_at:
            created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        text = str(cgi.escape(content['mblog']['text'])).replace("\'", '"')
        content_lists.append((user_id, content_id, created_at, text))
        # print content_id + ':' +created_at + ':' + text
    return tuple(content_lists)

def inser_follower_data(data):
    '''
    # 插入名称和相关的关注人数
    :param data:
    :return:
    '''
    if data != []:
        db = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_DATABASE, charset="utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        sql = "SELECT * FROM weibo_data \
                WHERE update_date = '%s' AND name = '%s'" % (date.today(), data[0])

        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()

        if results == ():
            data.append(str(date.today()))
            data = tuple(data)
            # SQL 插入语句
            sql = "INSERT IGNORE INTO weibo_data( \
                          name, follower_num, update_date) \
                          VALUES ('%s', '%d', '%s')" % \
                  data
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print u'插入成功'
            except Exception, e:
                # 发生错误时回滚
                db.rollback()
                print e
            # 关闭数据库连接
            db.close()
        else:
            print u'[!] 重复'

def get_content_count(id=''):
    '''
    # 取内容的总数量
    :param id:
    :return:
    '''
    res = get(url=API['content'].format(id, id))

    return res['cardlistInfo']['total']

def get_reply_count(id=''):
    '''
    # 取回复的总数量
    :param id:
    :return:
    '''
    res = get(url=API['content_in'].format(id))
    print res
    if res is types.StringType:
        print u'[!] 获取回复数量失败'
        return 0
    elif res is not types.StringType:
        return res['total_number']

def insert_content_data(datas=''):
    '''
    # 插入所有的微博内容
    :param datas:
    :return:
    '''
    db = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_DATABASE, charset="utf8")
    cursor = db.cursor()
    for data in datas:
        sql = "INSERT IGNORE INTO weibo_content(id, user_id, content_id, created_at, text) VALUES (null, '%s', '%s', '%s', '%s')"\
                %data
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except Exception, e:
            # 发生错误时回滚
            db.rollback()
            print u'插入错误' + ':' + str(e) + ':' + str(data)
        # 关闭数据库连接
    db.close()

def get_reply_by_content_id(id='', page=''):
    '''
    # 按照内容ID取回复列表
    :param id:
    :param page:
    :return:
    '''
    datas = list()
    for p in range(1, page):
        try:
            url = API['conteng_in_with_page'].format(id, p)
            res = get(url=url)
            if res == '':
                print u'[!] 中断在:' + str(p)
                return datas
            else:
                ds = res['data']
        except Exception, e:
            print 'get_reply_by_content_id:page:' + str(p) + ':' + str(e) + ':' + str(url)
        print p
        if p%50 == 0:
            time.sleep(1)
        else:
            time.sleep(0.1)
        for data in ds:
            reply_id = str(data['id'])
            created_at = data['mblog']['created_at'].replace(u'今天', str(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
            if u'分钟' in created_at:
                created_at = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
            text = str(data['text'])
            text = str(cgi.escape(text)).replace("\'", '"')
            user = data['user']['screen_name']
            datas.append((id, reply_id, created_at, text, user))
    return datas

def insert_reply(datas=''):
    '''
    # 插回复数据
    :param datas:
    :return:
    '''
    db = MySQLdb.connect(DB_IP, DB_USER, DB_PASSWORD, DB_DATABASE, charset="utf8")
    cursor = db.cursor()
    for data in datas:
        sql = "INSERT IGNORE INTO weibo_reply( \
                id, content_id, reply_id, created_at, text, user) \
                VALUES (null, '%s', '%s', '%s', '%s', '%s')" % \
              data
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            # time.sleep(0.1)
        except Exception, e:
            # 发生错误时回滚
            db.rollback()
            print u'[!] 插入错误' + ':' + str(data[3])
            print e
            # 关闭数据库连接
    db.close()

def get_user_id_by_name(name=''):
    '''
    # 用名称转换成id+name tuple
    :param name:
    :return:
    '''
    url = 'http://m.weibo.cn/n/{0}'.format(urllib.quote(name))
    try:
        u = requests.get(url=url, allow_redirects=False).headers['Location']
    except Exception,e:
        print u'[!] {0}:没找到Location'.format(name)
        return ()

    id = str(u).split('/')[2]

    count = get_follower_count(id=id)

    if check_is_idol(id=id):
        return (id, name)
    else:
        print u'[!] {0}:可能不是idol账户'.format(name)
        return ()

def check_is_idol(id):
    '''
    # 依照粉丝数判断是否为偶像
    :param id:
    :return:
    '''
    count = get_follower_count(id=id)
    if count >= 10000:
        return True
    else:
        return False

if __name__ == '__main__':
    pass
    # 取所有snh48成员的名字
    # !!失败操作
    # users = snh48_data.get_users(url='http://www.snh48.com/member_list.php')
    # for user in users:
    #     res = get_user_id_by_name(name='SNH48-{0}-'.format(user))
    #     if res != ():
    #         id = res[0]
    #         print '[+] {0}:{1}:找到该用户'.format(user, id)
    #     else:
    #         res = get_user_id_by_name(name='SNH48-{0}'.format(user))
    #         if res != ():
    #             id = res[0]
    #             print '[+] {0}:{1}:找到该用户'.format(user, id)

    # 插入粉丝数
    # data = get_follower_count(id='5863498042')
    # inser_follower_data(data)

    # 爬内容，仅一页，用于触发更新
    # datas = get_content_list(id='5863498042')
    # print datas.__len__()
    # insert_content_data(datas=datas)

    # 抓单个人所有微博
    # count = get_content_count(id=USERS['SNH48-黄彤扬'])
    # page = (count/10)+1
    # datas = get_content_with_page_list(id=USERS['SNH48-黄彤扬'], count=page)
    # insert_content_data(datas=datas)
    # print 'done'

    # 爬单个微博的所有评论
    # page = int(get_reply_count(id='4081165431996283'))/10+1
    # print page
    # datas =  get_reply_by_content_id(id='4081165431996283', page=page)
    # print datas
    # insert_reply(datas=datas)

    # 从名字到插入粉丝数
    # id = get_user_id_by_name(name='SNH48-鞠婧祎')[0]
    # print id
    # id = '5460951688'
    # data = get_follower_count(id=id)
    # inser_follower_data(data)

    # 遍历字典，插入粉丝数
    for key,value in USERS.items():
        id = value
        data = get_follower_count(id=id)
        if data == []:
            break
        inser_follower_data(data)

    # check_ip_proxy()