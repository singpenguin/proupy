#!/usr/bin/env python
# coding: utf-8

import web,sys
from config.settings import db
from config.settings import col_polity
from config.settings import col_polity_comment
from config.settings import render
from config.settings import config
from models import base
from datetime import datetime
import admin

reload(sys)
sys.setdefaultencoding('utf8')

class Index:
    def GET(self,name):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        list_news = db[col_polity].find({'authorUrl':name}).sort('date',-1).limit(10)
        if not list_news:
            raise web.seeother(config.url+"/404")
        count = db[col_polity].find({'authorUrl':name}).count()
        pagecount = base.format_pagecount(count)
        rand_news = base.get_rand_news()
        #设置作者结果的页面标题
        config.title = name + '的所有文章'
        return render.polity_result(name,list_news,1,pagecount,
                                    base.tag_cache,rand_news)

class ArticleView:
    def GET(self,artno):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        artno = int(artno)
        arc = db[col_polity].find_one({'_id':artno,'status':'publish','cmt_status':'open'})
        if not arc:
            raise web.seeother(config.url+"/404")
        _comment = list(db[col_polity_comment].find({'postid':artno}).sort('date',1))
        import md5
        for x in _comment:
            if x['email']:
                x['email'] = "http://www.gravatar.com/avatar/" + md5.md5(x['email'].lower()).hexdigest()
            else:
                x['email'] = "$config.static/images/default_avatar.jpg"
        #在没有错误的情况下阅读次数加1
        db[col_polity].update({'_id':artno},{'$inc':{'click':1}})
        rand_news = base.get_rand_news()
        #设置一下页面的标题
        config.title = arc['title']
        return render.news(arc,_comment,base.tag_cache,rand_news,isNet="polity")

class ArticlePage:
    def GET(self,name,pageno):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        pageno = int(pageno)
        list_news = db[col_polity].find({'authorUrl':name,'status':'publish','cmt_status':'open'}).sort('date',-1).skip((pageno-1)*10).limit(10)
        if not list_news:
            raise web.seeother(config.url+"/404")
        count = db[col_polity].find({'authorUrl':name}).count()
        pagecount = base.format_pagecount(count)
        rand_news = base.get_rand_news()
        #设置作者结果的页面标题
        config.title = name + '的所有文章'
        return render.polity_result(name,list_news,pageno,pagecount,
                                    base.tag_cache,rand_news)
class ArticleComment:
    def POST(self,id):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        id = int(id)
        i = web.input(name='',email='',url=None,message='')
        if i.name and i.message and i.email:
            import re
            foo = re.match("^[\\w-]+(\\.[\\w-]+)*@[\\w-]+(\\.[\\w-]+)+$", i.email)
            if foo:
                if i.url == "http://":
                    i.url = ""
                from datetime import datetime
                db[col_polity_comment].insert({'postid':id,'author':i.name,
                                        'email':i.email.rstrip(),'url':i.url,
                                        'ip':web.ctx.ip,'date':datetime.now(),
                                        'content':i.message,'_id':base.getLastID(col_polity_comment)})
                db[col_polity].update({'_id':id},{'$inc':{'cmt_count':1}})
                for news in base.newsCache:
                    if news['_id'] == id:
                        news['cmt_count'] += 1
        referer = web.ctx.env.get('HTTP_REFERER', config.url)
        return web.seeother(referer)
    
class New:
    def POST(self):
        i = web.input()
        author = i.get("author")
        authorUrl = i.get("authorUrl")
        original_desc = i.get("original_desc")
        original_src = i.get("original_src")
        title = i.get("title")
        content = i.get("content1")
        post_status = i.get("post_status")
        comment_status = i.get("comment_status")
        post_date = str2time(i.get("post_date"))
        tag = i.get("tag")
        if not author or not title or not content \
            or not post_status or not comment_status \
            or not post_date:
            return render.admin.NewArticle()
        db[col_polity].insert({'author':author,'original_desc':original_desc,
                               'original_url':original_src,'date':post_date,
                               'content':content,'title':title,
                               'status':post_status,'cmt_status':comment_status,
                               'keywords':tag,'_id':base.getLastID(col_polity),
                               'ding':0,'click':0,'cai':0,'cmt_count':0,
                               'authorUrl':authorUrl})
        return render.admin.NewArticle()

def str2time(s):
    l = s.split(' ')
    y = [int(x) for x in l[0].split('-')]
    t = [int(x) for x in l[1].split(':')]
    return datetime(y[0],y[1],y[2],t[0],t[1],t[2])
