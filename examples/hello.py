#!/usr/bin/env python
# encoding:utf-8
#
# This is an example of how to use the proupy.
#

import sys
import proupy.web
import proupy.wsgi

class Index(proupy.web.HTTPRequest):
	def GET(self):
		return "Hello word"

class Test(proupy.web.HTTPRequest):
	def GET(self, arg):
		return "Hello %s" % arg

url = [("/", Index),
		("/(.*)", Test)]


application = proupy.wsgi.Application(url)


if __name__ == "__main__":
	from gevent import monkey;monkey.patch_all()
	from gevent.pywsgi import WSGIServer
	if len(sys.argv) > 1:
		if sys.argv[1].isdigit():
			print("http://localhost:"+sys.argv[1])
			WSGIServer(("" ,int(sys.argv[1])),application).serve_forever()
		else:
			print("invalid parameters")
	else:
		print("http://localhost:8080")
		WSGIServer(("" , 8080),application).serve_forever()
