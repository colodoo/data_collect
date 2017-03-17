#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/2/20 22:23
# @Author  : CoLoDoo
# @Site    : 
# @File    : app.py
# @Software: PyCharm

from flask import Flask, render_template, request
from pet_58data import data58

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'ok'

@app.route('/pet/<city>', methods=['GET'])
def pet_58data(city):
    infos = data58.get_hour_pet_infos('http://'+ city +'.58.com/cwzengsong/')
    results = []
    for info in infos:
        tmp = data58.get_detail_in_url(info['url'], title=info['title'], date=info['date'])
        results.append(tmp)
    print results
    return render_template('pet.html', results=results, city=city)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True)
