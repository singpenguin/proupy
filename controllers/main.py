#!/usr/bin/env python
# coding: utf-8

import web,sys
from config.settings import db,render,config
from models import base
import random

reload(sys)
sys.setdefaultencoding('utf8')

class Index:
	def GET(self):
		s = unicode(random.choice(base.mingyan), 'gbk')
		config.title = 'Proupy.com'
		return render.index(base.newsCache[0:6],
						base.latest_comments,1,base.pagecount,
						base.tag_cache,s)


class ArticlePage:
	def GET(self, id):
		id = int(id)
		arc = db[col_post].find_one({'_id':id,'status':'publish','cmt_status':'open'})
		if arc:
			_comment = list(db[col_comment].find({'postid':id}).sort('date',1))
			import md5
			for x in _comment:
				if x['email']:
					x['email'] = "http://www.gravatar.com/avatar/" + md5.md5(x['email'].lower()).hexdigest()
				else:
					x['email'] = "$config.static/images/default_avatar.jpg"
			#在没有错误的情况下阅读次数加1，缓存中也要加1
			db[col_post].update({'_id':id},{'$inc':{'click':1}})
			for news in base.newsCache:
				if news['_id'] == id:
					news['click'] += 1
			rand_news = base.get_rand_news()
			#设置一下页面的标题
			config.title = arc['title']
			return render.news(arc,_comment,base.tag_cache,rand_news)
		else:
			#返回404
			return web.seeother(config.url+"/404")

class CommentAdd:
	def POST(self, id):
		id = int(id)
		i = web.input(name='',email='',url=None,message='')
		if i.name and i.message and i.email:
			import re
			foo = re.match("^[\\w-]+(\\.[\\w-]+)*@[\\w-]+(\\.[\\w-]+)+$", i.email)
			if foo:
				if i.url == "http://":
					i.url = ""
				from datetime import datetime
				db[col_comment].insert({'postid':id,'author':i.name,
						'email':i.email.rstrip(),'url':i.url,
						'ip':web.ctx.ip,'date':datetime.now(),
						'content':i.message,'_id':base.getLastID(col_comment)})
				db[col_post].update({'_id':id},{'$inc':{'cmt_count':1}})
				for news in base.newsCache:
					if news['_id'] == id:
						news['cmt_count'] += 1
				#添加完评论后更新了下最近15条评论
				base.latest_comments = base.set_latest_comments()
		referer = web.ctx.env.get('HTTP_REFERER', config.url)
		return web.seeother(referer)

class NewsPageList:
	def GET(self, id):
		#这里需要注意一下传递过来的ID为unicode类型，需要转换一下
		n = int(id)
		if n < 4:
			news = base.newsCache[(n-1)*6:n*6]
		else:
			news = db[col_post].find({'status':'publish','cmt_status':'open'}).sort('_id',-1).skip((n-1)*6).limit(6)
		if news:
			s = unicode(random.choice(base.mingyan), 'gbk')
			config.title = 'Proupy.com'
			return render.index(news, base.latest_comments, n,base.pagecount,
							base.tag_cache,s)
		else:
			#404
			return web.seeother(config.url+"/404")
        

class Author:
	def GET(self, name):
		#查询到数据后才继续下面
		list_news = db[col_post].find({'author':name,'status':'publish','cmt_status':'open'}).sort('date',-1).limit(10)
		if not list_news:
			#404
			raise web.seeother(config.url+"/404")
		count = db[col_post].find({'author':name}).count()
		pagecount = base.format_pagecount(count)
		rand_news = base.get_rand_news()
		#设置作者结果的页面标题
		config.title = name + '的所有文章'
		#下面的123只用来占位用，表示这是作者页
		return render.result(name,list_news,"123",1,pagecount,
					base.tag_cache,rand_news)

class AuthorPageList:
	def GET(self,name,id):
		n = int(id)
		#查询到数据后才继续下面
		list_news = db[col_post].find({'author':name,'status':'publish','cmt_status':'open'}).sort('date',-1).skip((n-1)*10).limit(10)
		if not list_news:
			#404
			raise web.seeother(config.url+"/404")
		count = db[col_post].find({'author':name}).count()
		pagecount = base.format_pagecount(count)
		rand_news = base.get_rand_news()
		config.title = name + '的所有文章'
		return render.result(name,list_news,"123",n,pagecount,base.tag_cache,rand_news)

class Comments:
	def GET(self, id=1):
		#所有的评论
		id = int(id)
		cmts = list(db[col_comment].find().sort('date',-1).skip((id-1)*10).limit(10))
		import md5
		for x in cmts:
			x['title'] = db[col_post].find_one({'_id':x['postid']})['title']
			if x['email']:
				x['email'] = "http://www.gravatar.com/avatar/" + md5.md5(x['email'].lower()).hexdigest()
			else:
				x['email'] = "$config.static/images/default_avatar.jpg"
		if not cmts:
			raise web.seeother(config.url+"/404")
		count = db[col_ids].find_one({'name':col_comment})['id']
		pagecount = base.format_pagecount(count)
		rand_news = base.get_rand_news()
		config.title = '最新评论'
		return render.news_cmts(cmts,id,pagecount,base.tag_cache,rand_news)

class TagView:
	def GET(self,name):
		list_news = db[col_post].find({'keywords':{'$regex':name,'$options':'i'},'status':'publish','cmt_status':'open'}).sort('date',-1).limit(10)
		if not list_news:
			#404
			raise web.seeother(config.url+"/404")
		count = db[col_post].find({'keywords':{'$regex':name,'$options':'i'}}).count()
		pagecount = base.format_pagecount(count)
		rand_news = base.get_rand_news()
		config.title = name + '下面的所有文章'
		return render.result(name,list_news,'',1,pagecount,base.tag_cache,rand_news)

class TagPageList:
	def GET(self,name,id):
		n = int(id)
		list_news = db[col_post].find({'keywords':{'$regex':name,'$options':'i'},'status':'publish','cmt_status':'open'}).sort('date',-1).skip((n-1)*10).limit(10)        
		if not list_news:
			#404
			raise web.seeother(config.url+"/404")
		count = db[col_post].find({'keywords':{'$regex':name,'$options':'i'}}).count()
		pagecount = base.format_pagecount(count)
		rand_news = base.get_rand_news()
		config.title = name + '下面的所有文章'
		return render.result(name,list_news,'',n,pagecount,base.tag_cache,rand_news)

class NotFound:
	def GET(self):
		return render.not_found()

class other:
	def GET(self,name):
		raise web.seeother(config.url+"/404")

#控制顶和踩
class SetDingCai:
	def GET(self,id,n):
		id = int(id)
		n = int(n)
		if not id:
			return
		if n==1:   
			rs = db[col_post].find_and_modify(query={'_id':id},update={'$inc':{'ding':1}})
		else:
			rs = db[col_post].find_and_modify(query={'_id':id},update={'$inc':{'cai':1}})
		if rs:
			if n:
				return 1
			else:
				return 0
