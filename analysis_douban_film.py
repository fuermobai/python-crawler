# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 12:41:36 2019

@author: fuermobai
"""

import pandas as pd
df = pd.read_excel('douban_film_index.xlsx',sheet_name=0)

df['score_cnt'] = df['score_cnt'].map(lambda x: int(x[:-3]))
df.describe()['score_cnt']

df_tmp = df[['director','writers','actors', 'types', 'dates', 'play_location', 'rating_per', 'betters', 'tags']]

df[['director', 'writers', 'actors', 'types', 'dates', 'play_location', 'rating_per', 'betters', 'tags']] = df_tmp.applymap(lambda x: eval(x))

df['dates'] = df['dates'].map(lambda x: [int(i) for i in x])
df['year'] = df['dates'].map(lambda x: min(x))  # year是新添加的

df['five_star_rate'] = df['rating_per'].map(lambda x: float(x[0][:-1])/100)
df['favor_rate'] = df['rating_per'].map(lambda y:(float(y[0][:-1])+float(y[1][:-1]))/100)

df['better_than'] = df['betters'].map(lambda x : sum([int(i.split('%')[0]) for i in x])/len(x))

from functools import reduce
df['director'] = df['director'].map(lambda x: [i.strip() for i in x])

director_list = reduce(lambda x,y : x+y,df.director)
print(len(director_list))

from collections import Counter

dire_counter = Counter(director_list)
dire_counter = sorted(dire_counter.items(),key=lambda x: x[1],reverse=True)
top_directors = list(filter(lambda x: x[1] >=3,dire_counter))
print(top_directors)

from collections import defaultdict
top_dire_score = defaultdict(list)
top_dire_ind = defaultdict(list)
for name,cnt in top_directors:
    for index,row in df.iterrows():
        if name in row['director']:
            top_dire_score[name].append(row['score'])
            top_dire_ind[name].append(row['top_no'])
print(top_dire_score)
print(top_dire_ind)

from math import log2
from math import sqrt
rank_score = []
rank_ind = []

for name,scores in top_dire_score.items():
    rank_score.append([name,sum(scores)/len(scores)*sqrt(log2(len(scores)))])
    
for name,indexes in top_dire_ind.items():
    rank_ind.append([name,sum(indexes)/sqrt(log2(len(scores)))/len(indexes)])
    
rank_score = sorted(rank_score,key=lambda x: x[1],reverse=True)
rank_ind = sorted(rank_ind,key=lambda x:x[1])

print(rank_score[:10])
print(rank_ind[:10])
















