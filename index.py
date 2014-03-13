#!/usr/bin/env python
# encoding:utf-8

import sys
import proupy.web
import proupy.wsgi

class Index(proupy.web.HTTPRequest):
	def GET(self):
		return {'a':'abcdefg', 'b':2},"sadfkiwofe"
		return "Hello word"
	def POST(self):
		print(self.request.headers)
		print(self.request.body)
		return "aaa"

url = [("/", Index)]


application = proupy.wsgi.Application(url)


if __name__ == "__main__":
	from gevent import monkey;monkey.patch_all()
	from gevent.pywsgi import WSGIServer
	"""
	def hack_fileobject_close():
		if getattr(socket._fileobject.close, '__hacked__', None):
			return
		old_close = socket._fileobject.close
		def new_close(self, *p, **kw):
			try:
				return old_close(self, *p, **kw)
			except Exception, e:
				print("Ignore %s." % str(e))
		new_close.__hacked__ = True
		socket._fileobject.close = new_close
	#hack_fileobject_close()
	"""

	if len(sys.argv) > 1:
		if sys.argv[1].isdigit():
			print("http://localhost:"+sys.argv[1])
			WSGIServer(("" ,int(sys.argv[1])),application).serve_forever()
		else:
			print("invalid parameters")
	else:
		print("invalid parameters")
