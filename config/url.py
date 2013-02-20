#!/usr/bin/env python
# coding: utf-8

pre_fix = 'controllers.'

urls = (
	'/',									pre_fix + 'main.Index',
	'/news/(\d+)',							pre_fix + 'main.ArticlePage',
	'/news/(\d+)/comment',					pre_fix + 'main.CommentAdd',
	'/news/page/(\d+)',						pre_fix + 'main.NewsPageList',
	'/news/cmts',							pre_fix + 'main.Comments',
	'/news/cmts/page/(\d+)',				pre_fix + 'main.Comments',
	'/author/(.*)/page/(\d+)',				pre_fix + 'main.AuthorPageList',
	'/author/(.*)',							pre_fix + 'main.AuthorView',
	'/tag/(.*)/page/(\d+)',					pre_fix + 'main.TagPageList',
	'/tag/(.*)',							pre_fix + 'main.TagView',
	'/setDingCai/(\d+)/(\d+)',				pre_fix + 'main.SetDingCai',
	'/404',									pre_fix + 'main.NotFound',

	'/feed',								pre_fix + 'admin.GenerateFeed',

	'/libs',								pre_fix + 'libs.libsPage',
	'/libs/(\d+)',							pre_fix + 'libs.libsItem',
	'/libs/page/(\d+)',						pre_fix + 'libs.libsPage',
	'/libs/(\d+)/comment',					pre_fix + 'libs.libsComment',

	'/framework',							pre_fix + 'libs.framePage',
	'/framework/(\d+)',						pre_fix + 'libs.frameworkItem',
	'/framework/page/(\d+)',				pre_fix + 'libs.libsPage',
	'/framework/(\d+)/comment',				pre_fix + 'libs.libsComment',

	#'/(?:css|img|js|rss)/.+',				pre_fix + 'public.public',
	#r'/robots\.txt',						pre_fix + 'public.public',
	#r'/sitemap\.xml',						pre_fix + 'public.public',

	'/admin/logins',						pre_fix + 'admin.Login',
	'/admin/article/new',					pre_fix + 'admin.NewArticle',
	'/admin/article/edit',					pre_fix + 'admin.ArticleEdit',
	'/admin/upload',						pre_fix + 'admin.Upload',
	'/admin/author/new',					pre_fix + 'admin.NewAuthor',
	'/admin/libs/new',						pre_fix + 'libs.New',
	'/admin/netart/new',					pre_fix + 'polity.New',
	'/admin/generatesitemap',				pre_fix + 'admin.GenerateSitemap',

	'/(zhicheng95|skyinwell|botaokk001)',	pre_fix + 'polity.Index',
	'/polity/(\d+)',						pre_fix + 'polity.ArticleView',
	'/(zhicheng95|skyinwell|botaokk001)/page/(\d+)',	pre_fix + 'polity.ArticlePage',
	'/polity/(\d+)/comment',				pre_fix + 'polity.ArticleComment',

	'/(.*)',								pre_fix + 'main.other',
)
