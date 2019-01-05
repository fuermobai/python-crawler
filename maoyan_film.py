# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 14:49:48 2019

@author: fuermobai
"""

import matplotlib as mpl
mpl.use('agg')
import requests
import re
import pandas as pd
import time
import seaborn as sns
sns.set()
mpl.rcParams['font.sans-serif']=[u'SimHei']
mpl.rcParams['axes.unicode_minus']=False

urls = ['http://maoyan.com/board/4?offset={0}'.format(i) for i in range(0,100,10)]
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}


def get_one_page(url,headers):
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.content.decode('utf-8')
    return None

data=[]
for url in urls:
    tmp = get_one_page(url,headers=headers)
    if not tmp == None:
        data.append(tmp)
    time.sleep(.5)
print('{0} pages crawled'.format(len(data)))

actor_pattern = re.compile('<p\sclass="star">\s*(.*?)\s*</p>',re.S)
title_pattern = re.compile('class="name".*?movieId.*?>(.*?)</a></p>', re.S)
index_pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>', re.S)
time_pattern = re.compile('<p\sclass="releasetime">(.*?)</p>', re.S)
score_pattern = re.compile('<p\sclass="score"><i\sclass="integer">(\d+)\.</i><i\sclass="fraction">(\d+)</i></p>', re.S)

indexes = []
actors = []
titles = []
release_times = []
scores = []

for page in data:
    indexes.extend(re.findall(index_pattern,page))
    titles.extend(re.findall(title_pattern,page))
    actors.extend(re.findall(actor_pattern,page))
    release_times.extend(re.findall(time_pattern,page))
    scores.extend(re.findall(score_pattern,page))
    
actors = [i.strip('主演：') for i in actors]
locs = [i.strip('上映时间：')[10:].strip('()') if len(i.strip('上映时间：')) > 10 else '中国' for i in release_times]
release_times = [i.strip('上映时间：')[:10] for i in release_times]
scores = [int(i) + int(j)/10 for i,j in scores]

df = pd.DataFrame({
        'rank': indexes,
        'title': titles,
        'actor': actors,
        'release_time': release_times,
        'score': scores,
        'location': locs
        })

df = df[['rank','title','actor','score','location','release_time']]
df.to_csv('./maoyan_top100_movie.csv',index=False)

df.head()
df['上映年份'] = df['release_time'].map(lambda x: int(x[:4]))
df['上映年份'].value_counts()
df['上映年份区间'] = pd.cut(df['上映年份'],bins=[1938,1980,1990,1995,2000,2005,2010,2015,2018])
pic=df['上映年份区间'].value_counts().sort_index().plot(kind='bar')
pic.figure