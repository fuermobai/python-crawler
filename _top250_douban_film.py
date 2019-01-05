#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 22:17:03 2019

@author: libre
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import time
import re

class DoubanMovieTop():
    def __init__(self):
        self.top_urls = ['https://movie.douban.com/top250?start={0}&filter='.format(x*25) for x in range(10)]
        self.data = defaultdict(list)
        self.columns = ['title','link','score','score_cnt','top_no','director','writers', 'actors', 'types',
                        'edit_location', 'language', 'dates', 'play_location', 'length', 'rating_per', 'betters',
                        'had_seen', 'want_see', 'tags', 'short_review', 'review', 'ask', 'discussion']
        
        self.df = None
        
    def get_bsobj(self,url):
        html = urlopen(url).read().decode('utf-8')
        bsobj = BeautifulSoup(html,'lxml')
        return bsobj
    
    def get_info(self):
        for url in self.top_urls:
            bsobj = self.get_bsobj(url)
            main = bsobj.find('ol',{'class':'grid_view'})
            
            title_objs = main.findAll('div',{'class':'hd'})
            titles = [i.find('span').text for i in title_objs]
            links = [i.find('a')['href'] for i in title_objs]
            
            score_objs = main.findAll('div',{'class':'star'})
            scores = [i.find('span',{'class':'rating_num'}).text for i in score_objs]
            score_cnts = [i.findAll('span')[-1].text for i in score_objs]
            
            for title,link,score,score_cnt in zip(titles,links,scores,score_cnts):
                self.data[title].extend([title,link,score,scscore_cnt])
                bsobj_more = self.get_bsobj(link)
                more_data = self.get_more_info(bsobj_more)
                self.data[title].extend(more_data)
                print(self.data[title])
                print(len(self.data))
                time.sleep(1)
            
            
            
            
            
            
            
            
            