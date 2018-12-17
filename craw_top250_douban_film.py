#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 22:04:11 2018

@author: libre
"""

import requests
from bs4 import BeautifulSoup
start = 0
for n in range(0,10):
    html = requests.get('https://movie.douban.com/top250?start='+str(start))
    start += 25
    soup = BeautifulSoup(html.text, 'html.parser')
    for item in soup.find_all('div',"info"):
        title = item.div.a.span.string
        yearline = item.find('div','bd').p.contents[2].string
        yearline = yearline.replace(' ','')
        yearline = yearline.replace('\n','')
        year = yearline[0:4]
        print(year)
    