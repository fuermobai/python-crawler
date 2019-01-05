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
            scores = [i.find('span', {'class': 'rating_num'}).text for i in score_objs]
            score_cnts = [i.findAll('span')[-1].text for i in score_objs]
            
            for title,link,score,score_cnt in zip(titles,links,scores,score_cnts):
                self.data[title].extend([title,link,score,score_cnt])
                bsobj_more = self.get_bsobj(link)
                more_data = self.get_more_info(bsobj_more)
                self.data[title].extend(more_data)
                print(self.data[title])
                print(len(self.data))
                time.sleep(1)
                
                
                
    def get_more_info(self,bsobj):
        top_no = bsobj.find('span',{'class':'top250-no'}).text.split('.')[1]
        
        main = bsobj.find('div',{'id':'info'})
        
        dire_obj = main.findAll('a',{'rel':'v:directedBy'})
        director = [i.text for i in dire_obj]
        
        try:
            writer_obj = main.findAll('span',{'class':'attrs'})[1]
            writers = [i.text for i in writer_obj.findAll('a')]
        except Exception as e:
                writers = []
                print(e)
            
        try:
            actor_obj = main.findAll('a',{'rel':'v:starring'})
            actors = [i.text for i in actor_obj]
        except Exception as e:
                actors = []
                print(e)
            
        type_obj = main.findAll('span',{'property':'v:genre'})
        types = [i.text for i in type_obj]
        
        pattern = re.compile('地区:(.*?)\n语言',re.S)

        edit_location = re.findall(pattern, main.text)[0]
        
        pattern2 = re.compile('语言:(.*?)\n上映日期')
        language = re.findall(pattern2,main.text)[0]
        
        date_obj = main.findAll('span',{'property':'v:initialReleaseDate'})
        dates = [i.text.split( '(' )[0][:4] for i in date_obj]
        play_location = [i.text.split( '(' )[1][:-1] for i in date_obj]
        
        length = main.find('span',{'property':'v:runtime'})['content']
        
        rating_obj = bsobj.findAll('span',{'class':'rating_per'})
        rating_per = [i.text for i in rating_obj]
        
        better_obj = bsobj.find('div',{'class':'rating_betterthan'})
        betters = [i.text for i in better_obj.findAll('a')]
        
        watch_obj = bsobj.find('div',{'class':'subject-others-interests-ft'})
        had_seen = watch_obj.find('a').text[:-3]
        want_see = watch_obj.findAll('a')[-1].text[:-3]
        
        tag_obj = bsobj.find('div',{'class':'tags-body'}).findAll('a')
        tags = [i.text for i in tag_obj]
        
        short_obj = bsobj.find('div',{'id':'comments-section'})
        short_review = short_obj.find('div').find('span',{'class':'pl'}).find('a').text.split(' ')[1]
        
        review = bsobj.find('a',{'href':'reviews'}).text.split(' ')[1]
        
        ask_obj = bsobj.find('div',{'id':'askmatrix'})
        ask = ask_obj.find('h2').find('a').text.strip()[2:-1]
        
        discuss_obj = bsobj.find('p',{'class':'pl','align':'right'}).find('a')
        #discussion = discuss_obj.text.strip().split( '(' )[1][2:-2]
        discussion = discuss_obj.text.strip().split('（')[1][2:-2]
        
        more_data = [top_no,director,writers,actors,types,edit_location,language,dates,play_location,length,rating_per,betters,had_seen,want_see,tags,short_review,review,ask,discussion]
        
        return more_data
            
    def dump_data(self):
        data = []
        for title,value in self.data.items():
            data.append(value)
        self.df = pd.DataFrame(data,columns=self.columns)
        self.df.to_csv('douban_top250films_info.csv',index=False)
            
        
if __name__ == '__main__':
    douban = DoubanMovieTop()
    douban.get_info()
    douban.dump_data()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
            
            
            
            