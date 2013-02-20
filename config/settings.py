#!/usr/bin/env python
# coding: utf-8
import web,pymongo

con = pymongo.Connection('localhost',27017)
db = con.proupy
col_ids = "ids"
col_post = "posts"
col_comment = "comments"
col_author = "author"
col_open = "opensource"
col_open_comment = "open_comments"
col_blacklist = "blacklist"
col_polity = "polity"
col_polity_comment = "polity_comments"

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
