#!/usr/bin/env python
# encoding:utf-8

import re
import traceback
import sys
from utils import safestr


class Application:
	def __init__(self, handlers=None, settings={"debug":False}):
		self.handlers = handlers or []
		self.init_mapping()
		self.settings = settings
		self.debug = settings['debug']

	def init_mapping(self):
		_handlers = []
		for h in self.handlers:
			_handlers.append((re.compile("^" + h[0] + "$"), h[1]))
		self.handlers = _handlers
		_handlers = None

	def __call__(self, env, start_response):
		for path,what in self.handlers:
			match = path.match(env['PATH_INFO'])
			if match:
				handle = what(env)
				args = [x for x in match.groups()]
				try:
					result = getattr(handle, env['REQUEST_METHOD'])(*args)
				except:
					print sys.stderr, traceback.format_exc()
					if not self.debug:
						result = "Internal Server Error"
					else:
						result = traceback.format_exc()
					handle.response.status = "500 Internal Server Error"
					#for x in handle.response.headers:
					#	if x[0] == "Content-Type":
					#		handle.response.headers.remove(x)
					#		handle.response.headers.append(('Content-Type', "text/plain; charset=UTF-8"))
					#		break
				#if "Content-Length" not in [k for k,_ in handle.response.headers]:
				#	handle.response.headers.append(('Content-Length', len(result)))
				#start_response(handle.response.status, [(k,v) for (k,v) in handle.response.headers.items()])
				start_response(handle.response.status, handle.response.headers)
				if hasattr(result, "next"):
					for x in result:
						yield x
				else:
					yield safestr(result)
				handle.cleanup()
				handle = None
				return 

		start_response('404 Not Found', [('Content-Type', 'text/html')])
		yield ['<h1>Not Found</h1>']
