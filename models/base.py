#!/usr/bin/env python
# coding: utf-8

'''
该类主要是存放页码，最近评论等，以做缓存之用,减少打开首页时读取数据库次数
一旦条件被激活，会重新为这些变量赋值
'''
from config.settings import db
from config.settings import config
from config.settings import col_post
from config.settings import col_comment
from config.settings import col_author
from config.settings import col_open
from config.settings import col_blacklist
import math


def isRefuseIP(ip):
    obj = db[col_blacklist].find_one({'ip':ip})
    if obj:
        return True
    return False
def getLastID(name):
    #获取某个集合的自增ID
    return db['ids'].find_and_modify(query={'name':name},update={'$inc':{'id':1}})['id']

def set_latest_comments():
    return list(db[col_comment].find().sort('date',-1).limit(15))
#获取总页数
def set_pagecount():
    count = db['ids'].find_one({'name':col_post})['id']
    return int(math.ceil(math.floor(count)/6))

#测试一下缓存三页的数据怎么样
def set_news_cache():
    return list(db[col_post].find({'status':'publish','cmt_status':'open'}).sort('_id',-1).limit(18))

#处理所有的标签
def set_tag_cache():
    temp = db[col_post].distinct('keywords')
    l = []
    for key in temp:
        if key in l:
            continue
        if ',' in key:
            t = key.split(",")
            for x in t:
                if x not in l:
                    l.append(x)
        else:
            l.append(key)
    return l

#随机选取10条记录作为随机文章
def get_rand_news():
    import random
    count = db['ids'].find_one({'name':'posts'})['id']
    return list(db[col_post].find({'_id':{'$in':random.sample(range(1,(count+1)),10)}}))

#格式化页码数
def format_pagecount(count):
    return int(math.ceil(math.floor(count)/10))

#读取名言警句
def read_mingyan():
    m = open(r'static/mingyan/mingyan.txt', 'r')
    l = m.readlines()
    m.close()
    return l

pagecount = set_pagecount()
latest_comments = set_latest_comments()
newsCache = set_news_cache()
tag_cache = set_tag_cache()
#rand_news = get_rand_news()
mingyan = read_mingyan()

#生成sitemap.xml文件
def generate_sitemap():
    import time
    url_list = []
    def create_dict(siteurl, lastmod, priority):
        m1 = {}
        #url可能还需要进行URL encode
        m1["loc"] = siteurl
        m1["lastmod"] = lastmod
        m1["changefreq"] = "daily"
        m1["priority"] = priority
        return m1

    site_libs_url = config.url+"/libs"
    site_framework_url = config.url+"/framework"    
    d = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    url_list.append(create_dict(config.url, d, "1.0"))
    #url_list.append(create_dict("http://www.proupy.com", d, "1.0"))
    url_list.append(create_dict(site_libs_url, d, "0.9"))
    url_list.append(create_dict(site_framework_url, d, "0.9"))    
    
    #访问数据库,文章表
    rows = db[col_post].find({},{'_id':1,'date':1})
    siteurl = config.url+"/news/"
    for row in rows:
        url_list.append(create_dict(siteurl+str(row['_id']),str(row['date'].date()),"0.8"))
    rows = db[col_open].find({},{'_id':1,'type':1})
    #开源表
    for row in rows:
        if row['type'] == "lib":
            url_list.append(create_dict(site_libs_url+"/"+str(row['_id']),d,"0.8"))
        else:
            url_list.append(create_dict(site_framework_url+"/"+str(row['_id']),d,"0.8"))
    #标签，可能有空格中文等，需要进行URL编码
    import urllib
    siteurl = config.url+"/tag/"
    for x in range(len(tag_cache)):
        temp = urllib.quote(tag_cache[x].encode("utf8"))
        url_list.append(create_dict(siteurl+temp,d,"0.9"))
    
    fh = open("static/sitemap.xml", "w")
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    fh.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    
    for m in url_list:
        fh.write("  <url>\n")
        fh.write("    <loc>"+m["loc"]+"</loc>\n")
        fh.write("    <lastmod>"+m["lastmod"]+"</lastmod>\n")
        fh.write("    <changefreq>"+m["changefreq"]+"</changefreq>\n")
        fh.write("    <priority>"+m["priority"]+"</priority>\n")
        fh.write("  </url>\n")
            
    fh.write("</urlset>")
    fh.close()

def generate_feed():
    #访问数据库,文章表
    rows = db[col_post].find().sort('_id',-1).limit(30)
    import time
    x = []
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    #dt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    dt = time.strftime(GMT_FORMAT, time.gmtime(time.time()))
    x.append('<?xml version="1.0" encoding="UTF-8"?>')
    x.append('<rss version="2.0">')
    x.append('<channel>')
    x.append('  <title>Python文章 教程 框架</title>')
    x.append('  <link>'+config.url+'</link>')
    x.append('  <description>关注Python</description>')
    x.append('  <pubDate>'+dt+'</pubDate>')
    x.append('  <lastBuildDate>'+dt+'</lastBuildDate>')

    linkurl = config.url+"/news/"
    for i,row in enumerate(rows):
        x.append('  <item id="'+str(i+1)+'">')
        x.append('    <title>'+row['title']+'</title>')
        x.append('    <link>'+linkurl+str(row['_id'])+'</link>')
        x.append('    <description><![CDATA['+row['summary']+']]></description>')
        x.append('    <pubDate>'+str(row['date'])+'</pubDate>')
        x.append('  </item>')
    
    x.append('</channel>')
    x.append('</rss>')
    return "\n".join(x)
