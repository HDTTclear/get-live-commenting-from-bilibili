# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:01:47 2020

@author: 16000
"""

import requests
from bs4 import BeautifulSoup
import collections
import jieba
import jieba.analyse
import re



#视频链接
archive_url_video="https://www.bilibili.com/video/BV1KA41187cr";
r_video = requests.get(archive_url_video)
#正则匹配获取弹幕链接
danmu_id = re.findall(r'cid=(\d+)&', r_video.text)[0]

#弹幕api
archive_url = "http://comment.bilibili.com/"+str(danmu_id)+'.xml';
r = requests.get(archive_url)
soup = BeautifulSoup(r.content, 'html5lib')
#标签提取，得到的links列表是全部弹幕
links = soup.findAll('d');


links_text=[];
counts_list=[];
#逐行词频分析并切分存储
for alink in links:
    atext=alink.get_text();
    links_text.append(atext);
    #print(atext);
    atext_cut=jieba.cut(atext,cut_all=True, HMM=False);
    #atext_cut=jieba.cut_for_search(atext);
    atext_cut_str=",".join(atext_cut);
    atext_counts=collections.Counter(atext_cut_str.split(','));
    counts_list.append(atext_counts);
    #alink['p']

#得到总体的词频
counts_sum=collections.Counter([]);
for counts in counts_list:
    counts_sum= counts_sum+counts;   




number_of_rank=20;
#切割后的    
top10=counts_sum.most_common(number_of_rank);
list(top10);
print(top10)


print('\n')

#整体的
counts_all=collections.Counter(links_text);    
top10_2=counts_all.most_common(number_of_rank);
print(top10_2)