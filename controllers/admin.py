#!/usr/bin/env python
# coding: utf-8

import web,sys
from config.settings import db
from config.settings import col_post
from config.settings import col_author
from config.settings import render
from models import base
from datetime import datetime


reload(sys)
sys.setdefaultencoding('utf8')

class Login:
	def GET(self):
		return render.admin.login()

	def POST(self):
		i = web.input()
		username = i.get("username", None)
		pw = i.get("pass", None)
		#如果有一个为空就返回重新登录
		if not username or not pw:
			return render.admin.login()
		obj = db[col_author].find_one({'name':username,'pass':pw})
		if obj:
			return render.admin.NewArticle()
		else:
			return render.admin.login()

#过滤文中的<,>&等
def htmlspecialchars(content):
	content = content.replace("&nbsp;", " ")
	content = content.replace("<br>", "\r\n")
	content = content.replace("<br>", "\n")
	content = tb_postcontent.replace("<br/>", "\n")
	content = content.replace("<br />", "\r\n")
	content = content.replace("&lt;", "<")
	content = content.replace("&gt;", ">")
	content = content.replace("&amp;", "&")
	return content

class NewArticle:
	def POST(self):
		i = web.input()
		author = i.get("author")
		original_desc = i.get("original_desc")
		original_src = i.get("original_src")
		title = i.get("title")
		content = i.get("content1")
		post_status = i.get("post_status")
		comment_status = i.get("comment_status")
		post_summary = i.get("post_summary")
		tag = i.get("tag")
		if not author or not title or not content \
				or not post_status or not comment_status \
				or not post_summary:
			return render.admin.NewArticle()
		#content = htmlspecialchars(content)
		db[col_post].insert({'author':author,'original_desc':original_desc,
				'original_url':original_src,'date':datetime.now(),
				'content':content,'title':title,
				'status':post_status,'summary':post_summary,
				'cmt_status':comment_status,'keywords':tag,
				'_id':base.getLastID(col_post),'ding':0,
				'click':0,'cai':0,'cmt_count':0})
		base.pagecount = base.set_pagecount()
		base.newsCache = base.set_news_cache()
		base.tag_cache = base.set_tag_cache()
		return render.admin.NewArticle()

class ArticleEdit:
	def POST(self):
		i = web.input()
		if i.get('artID'):
			obj = db[col_post].find_one({'_id':int(i.get('artID'))})
			return render.admin.article_edit(obj)
		author = i.get("author")
		original_desc = i.get("original_desc")
		original_src = i.get("original_src")
		title = i.get("title")
		content = i.get("content1")
		post_status = i.get("post_status")
		comment_status = i.get("comment_status")
		post_summary = i.get("post_summary")
		tag = i.get("tag")
		ding = int(i.get("ding"))
		cai = int(i.get("cai"))
		click = int(i.get("click"))
		_id = int(i.get("artID1"))
		db[col_post].update({'_id':_id},{'$set':{'author':author,
				'original_desc':original_desc,
				'original_url':original_src,
				'content':content,
				'title':title,
				'status':post_status,
				'summary':post_summary,
				'cmt_status':comment_status,
				'keywords':tag,'ding':ding,
				'cai':cai,'click':click}})
		base.newsCache = base.set_news_cache()
		return render.admin.NewArticle()
        
class NewAuthor:
	def POST(self):
		i = web.input()
		author = i.get("author")
		author_url = i.get("author_url")
		author_desc = i.get("author_desc")
		if not author:
			return render.admin.NewArticle()
		db[col_author].insert({'name':author,'author_desc':author_desc,
				'site':author_url,'pass':'123456',
				'_id':base.getLastID(col_author)})
		return render.admin.NewArticle()

class Upload:
	def POST(self):
		import os
		y = datetime.now().year
		m = datetime.now().month
		if not os.path.exists("static/uploads/"+str(y)):
			os.mkdir("static/uploads/"+str(y))
		if not os.path.exists("static/uploads/"+str(y)+"/"+str(m)):
			os.mkdir("static/uploads/"+str(y)+"/"+str(m))
		folder = "static/uploads/"+str(y)+"/"+str(m)+"/"
		i = web.input()
		uploaded = i.FileData
		if not uploaded:
			return
		try:
			_fl = open(folder+i.FileName, "wb")
			_fl.write(uploaded)
			_fl.close()
		except:
			if os.path.isfile(folder+i.FileName):
                os.remove(folder+i.FileName)
            return "except"
    
class GenerateSitemap:
	def GET(self):
		base.generate_sitemap()
		#通知谷歌已经更新sitemap
		#import os
		#os.system("wget -qO - http://www.google.com/webmasters/sitemaps/ping?sitemap=http://proupy.com")
		return "Generate sitemap OK!"

class GenerateFeed:
	def GET(self):
		web.header('Content-Type', 'text/xml; charset=utf-8')
		return base.generate_feed()
