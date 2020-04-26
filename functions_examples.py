# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 12:42:45 2020

@author: 16000
"""
import requests
from bs4 import BeautifulSoup
import collections
import jieba
import jieba.analyse
import re


#获得弹幕的链接
def get_live_commenting_url(archive_url_video):
    r_video = requests.get(archive_url_video)
#正则匹配获取弹幕链接
    danmu_id = re.findall(r'cid=(\d+)&', r_video.text)[0]
    archive_url = "http://comment.bilibili.com/"+str(danmu_id)+'.xml';

    return archive_url
#获得弹幕文本列表
def get live_commenting_text(archive_url_video):
    archive_url=get_live_commenting_url(archive_url_video);
    r = requests.get(archive_url)
    soup = BeautifulSoup(r.content, 'html5lib')
#标签提取，得到的links列表是全部弹幕
    links = soup.findAll('d');
    links_text=[];

#逐行词频分析并切分存储
    for alink in links:
        atext=alink.get_text();
        links_text.append(atext);    
    return links_text
#获得排名视频链接列表
def get_ranking_url():
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
    return video_links