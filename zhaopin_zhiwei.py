#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 22:35:37 2018

@author: libre
"""

url = 'https://www.zhipin.com/c101190400/h_101190400/?query=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&page=1'
headers={
        'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
page = 1
hud = ['职位名','薪资1','薪资2','职位名','地点','经验','学历','公司行业','融资阶段','公司人数','发布日期','发布人']
print(' '.join(hud))


import requests
from bs4 import BeautifulSoup
import time
for n in range(1,11):
    html = requests.get(url,headers=headers)
    page += 1
    soup = BeautifulSoup(html.text,'html.parser')
    for item in soup.find_all('div','job-primary'):
        shuchu=[]
        shuchu.append(item.find('div','job-title').string)
        
        xinzi=item.find('span','red').string
        xinzi=xinzi.replace('k','')
        xinzi=xinzi.split('-')
        shuchu.append(xinzi[0])
        shuchu.append(xinzi[1])
        
        yaoqiu=item.find('p').contents
        shuchu.append(yaoqiu[0].string if len(yaoqiu)>0 else 'None')
        shuchu.append(yaoqiu[2].string if len(yaoqiu)>2 else 'None')
        shuchu.append(yaoqiu[4].string if len(yaoqiu)>4 else 'None')
        
        gongsi = item.find('div','info-company').find('p').contents
        shuchu.append(gongsi[0].string if len(gongsi)>0 else 'None')
        shuchu.append(gongsi[2].string if len(gongsi)>2 else 'None')
        shuchu.append(gongsi[4].string if len(gongsi)>4 else 'None')
        
        shuchu.append(item.find('div','info-publis').find('p').string.replace('发布于',''))
        shuchu.append(item.find('div','info-publis').find('h3').contents[3].string)
        
        print(' '.join(shuchu))
        time.sleep(0.8)
