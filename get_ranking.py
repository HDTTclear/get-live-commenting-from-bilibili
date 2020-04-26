# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 11:39:05 2020

@author: 16000
"""
import requests
from bs4 import BeautifulSoup
import collections
import jieba
import jieba.analyse
import re

def get_counts_sum(archive_url_video):
    #archive_url_video="https://www.bilibili.com/video/BV1KA41187cr";
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

    return counts_sum



#得到热门视频
ranking_url="https://www.bilibili.com/ranking/all/0/0/30";#"https://www.bilibili.com/ranking";
#全站榜
#https://www.bilibili.com/ranking/all/0/0/3
#原创榜
#https://www.bilibili.com/ranking/origin/0/0/3
#第一个参数是分类，第二个参数是近期投稿/全部投稿，第三个参数是几日排行，

r=requests.get(ranking_url);
soup = BeautifulSoup(r.content,"lxml");
links = soup.findAll('a',attrs={'href':re.compile('^http')});
video_links = [ link['href'] for link in links];


counts_sum=collections.Counter([]);
for video_link in video_links:
    counts=get_counts_sum(video_link);
    counts_sum=counts_sum+counts;