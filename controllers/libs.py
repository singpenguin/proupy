#!/usr/bin/env python
# coding: utf-8

import web
from config.settings import db
from config.settings import col_open
from config.settings import col_open_comment
from config.settings import render
from config.settings import config
from models import base
from datetime import datetime
import admin


class libsItem:
    def GET(self, id):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        id = int(id)
        obj = db[col_open].find_one({'_id':id,'type':'lib'})
        if obj:
            _comment = list(db[col_open_comment].find({'openid':id}).sort('date',1))
            import md5
            
            for x in _comment:
                if x['email']:
                    x['email'] = "http://www.gravatar.com/avatar/" + md5.md5(x['email'].lower()).hexdigest()
                else:
                    x['email'] = "$config.static/images/default_avatar.jpg"
            rand_news = base.get_rand_news()
            config.title = obj['name']
            return render.lib_view("libs",obj,_comment,base.tag_cache,rand_news)
        else:
            raise web.seeother(config.url+"/404")

class frameworkItem:
    def GET(self, id):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        id = int(id)
        obj = db[col_open].find_one({'_id':id,'type':'framework'})
        if obj:
            _comment = list(db[col_open_comment].find({'openid':id}).sort('date',1))
            import md5
            
            for x in _comment:
                if x['email']:
                    x['email'] = "http://www.gravatar.com/avatar/" + md5.md5(x['email'].lower()).hexdigest()
                else:
                    x['email'] = "$config.static/images/default_avatar.jpg"
            rand_news = base.get_rand_news()
            config.title = obj['name']
            return render.lib_view("framework",obj,_comment,base.tag_cache,rand_news)
        else:
            raise web.seeother(config.url+"/404")

class libsPage:
    def GET(self, id=1):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        id = int(id)
        #将libs和libsPage都放这个类里面处理,默认就是第一页
        list_libs = db[col_open].find({'type':'lib'}).skip((id-1)*10).limit(10)
        if not list_libs:
            #404
            raise web.seeother(config.url+"/404")
        count = db[col_open].find({'type':'lib'}).count()
        pagecount = base.format_pagecount(count)
        rand_news = base.get_rand_news()
        #设置开源的页面标题
        config.title = 'Python开源类库'
        return render.libs('libs',list_libs,id,pagecount,base.tag_cache,rand_news)

class framePage:
    def GET(self, id=1):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        id = int(id)
        #将libs和libsPage都放这个类里面处理,默认就是第一页
        list_libs = db[col_open].find({'type':'framework'}).skip((id-1)*10).limit(10)
        if not list_libs:
            #404
            raise web.seeother(config.url+"/404")
        count = db[col_open].find({'type':'lib'}).count()
        pagecount = base.format_pagecount(count)
        rand_news = base.get_rand_news()
        #设置开源的页面标题
        config.title = 'Python开源框架'
        return render.libs('framework',list_libs,id,pagecount,base.tag_cache,rand_news)
    
class libsComment:
    def POST(self, id):
        if base.isRefuseIP(web.ctx.ip):
            raise web.seeother(config.url+"/404")
        id = int(id)
        i = web.input(name='',email='',url=None,message='')
        referer = web.ctx.env.get('HTTP_REFERER', config.url)
        if i.name and i.message and i.email:
            db[col_open_comment].insert({'openid':id,'author':i.name,
                                         'email':i.email,'url':i.url,
                                         'ip':web.ctx.ip,'date':datetime.now(),
                                         'content':i.message,
                                         '_id':base.getLastID(col_open_comment)})
        return web.seeother(referer)
    
class New:
    def POST(self):
        i = web.input()
        lib_name = i.get("lib_name")
        lib_url = i.get("lib_url")
        lib_desc = i.get("lib_desc")
        lib_content = i.get("lib_content")
        lib_type = i.get("lib_type")
        if not lib_name or not lib_url or not lib_desc or not lib_content or not lib_type:
            return render.admin.NewArticle(admin.get_author())
        db[col_open].insert({'name':lib_name,'site':lib_url,
                             'desc':lib_desc,'type':lib_type,
                             'content':lib_content,'_id':base.getLastID(col_open)})
        return render.admin.NewArticle()
