#!/usr/bin/env python
# coding: utf-8
import web,pymongo

con = pymongo.Connection('localhost',27017)
db = con.proupy

render = web.template.render('templates', cache=True)

web.config.debug = False

config = web.storage(
	email='proupy@163.com',
	url = 'http://localhost:8080',
	site_name = 'Test',
	static = '/static',
	title= '',
)


web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
