#!/usr/bin/env python
# encoding:utf-8

import Cookie
import urllib
import urlparse
from utils import Storage

class NoMethod:
	def __init__(self):
		status = '405 Method Not Allowed'
		headers = {"Content-Type": "text/html"}

class HTTPRequest(object):
	def __init__(self, environ):
		"""Parses the given WSGI environment to construct the request."""
		self.request = Storage()
		self.response = Storage()

		self.request.method = environ["REQUEST_METHOD"]
		self.request.protocol = environ["wsgi.url_scheme"]
		self.request.remote_ip = environ.get("REMOTE_ADDR", "")
		self.request.path = environ.get("PATH_INFO")
		if environ.get('QUERY_STRING'):
			self.request.query = '?' + environ.get('QUERY_STRING', '')
		else:
			self.request.query = ''
		self.request.fullpath = self.request.path + self.request.query
		self.request.version = "HTTP/1.1"
		self.request.headers = {}
		self.request.headers["Content-Type"] = environ.get("CONTENT_TYPE", "")
		self.request.headers["Content-Length"] = environ.get("CONTENT_LENGTH", "")
		for key in environ:
			if key.startswith("HTTP_"):
				self.request.headers[key[5:].replace("_", "-")] = environ[key]
		if self.request.headers.get("Content-Length"):
			self.request.body = environ["wsgi.input"].read(
				int(self.request.headers["Content-Length"]))
		else:
			self.request.body = ""
		if environ.get("HTTP_HOST"):
			self.request.host = environ["HTTP_HOST"]
		else:
			self.request.host = environ["SERVER_NAME"]

		self.response.status = "200 OK"
		#self.response.headers = {"Content-Type":"text/html; charset=UTF-8"}
		#如果设置了Content-Type，则必须设置Content-Length,设置了length,可不必设置type
		#如果不设置Content-Length，就容易出现[Errno 32]Broken pipe
		self.response.headers = []
		#self.response.headers = [("Content-Type","text/html; charset=UTF-8")]
		self.request.arguments = self.rawinput()
		self.initialize()

	def initialize(self):
		pass

	def supports_http_1_1(self):
		"""Returns True if this request supports HTTP/1.1 semantics"""
		return self.request.version == "HTTP/1.1"

	def rawinput(self, method="both"):
		method = method.lower()
		urlparams = urlparse.parse_qs(self.request.query[1:])
		if method == "url":
			return urlparams
		bodyparams = self._parse_body_arguments()
		if method == "body":
			return bodyparams or {}
		if bodyparams:
			for k,v in bodyparams.items():
				if k in urlparams:
					urlparams[k] += v
				else:
					urlparams[k] = v
		return urlparams

	def _parse_body_arguments(self):
		if self.request.headers['Content-Type'] == "application/x-www-form-urlencoded":
			return urlparse.parse_qs(self.request.body)
		elif self.request.headers['Content-Type'] in ("multipart/form-data", "application/octet-stream"):
			#去除开头和结尾的冗余字符
			tmpIndex = self.request.body.find('Content-Type')
			startIndex = 0
			if tmpIndex != -1:
				startIndex = self.request.body.find('\n', tmpIndex)+3

			endIndex = len(self.request.body)-2
			while True:
				if self.request.body[endIndex] == '\n': break
				else: endIndex -= 1
			#截取真实内容
			self.request.body = self.request.body[startIndex:endIndex-1]
			self.request.size = endIndex-startIndex-1

	def HEAD(self, *args, **kwargs):
		return NoMethod(self)

	def GET(self, *args, **kwargs):
		return NoMethod(self)

	def POST(self, *args, **kwargs):
		return NoMethod(self)

	def DELETE(self, *args, **kwargs):
		return NoMethod(self)

	def PATCH(self, *args, **kwargs):
		return NoMethod(self)

	def PUT(self, *args, **kwargs):
		return NoMethod(self)

	def OPTIONS(self, *args, **kwargs):
		return NoMethod(self)

	def set_header(self, name, value):
		for x in self.response.headers:
			if x[0] == name:
				self.response.headers.remove(x)
				break
		self.response.headers.append((name, value))

	def get_header(self, name):
		for x in self.response.headers:
			if x[0] == name:
				return x[1]
		return None

	def clear_header(self, name):
		for x in self.response.headers:
			if x[0] == name:
				self.response.headers.remove(x)
				break

	def cookies(self):
		"""A dictionary of Cookie.Morsel objects."""
		if not hasattr(self.request, "_cookies"):
			if "COOKIE" in self.request.headers:
				c = self.request.headers['COOKIE']
				if '"' in c:
					cookie = Cookie.SimpleCookie()
					try:
						cookie.load(c)
						self.request._cookies = dict((k, urllib.unquote(v.value)) for k, v in cookie.iteritems())
					except Exception:
						self.request._cookies = {}
				else:
					self.request._cookies = {}
					for key_value in c.split(';'):
						key_value = key_value.split('=', 1)
						if len(key_value) == 2:
							key, value = key_value
							self.request._cookies[key.strip()] = urllib.unquote(value.strip())
			else:
				self.request._cookies = {}
		return self.request._cookies

	def get_cookie(self, name, value=None):
		return self.cookies().get(name, value)

	def set_cookie(self, name, value, expires='', domain=None,
              secure=False, httponly=False, path="/"):
		morsel = Cookie.Morsel()
		morsel.set(name, value, urllib.quote(value))
		if expires < 0:
			expires = -1000000000
		morsel['expires'] = int(expires)
		morsel['path'] = path
		if domain:
			morsel['domain'] = domain
		if secure:
			morsel['secure'] = secure
		value = morsel.OutputString()
		if httponly:
			value += '; httponly'
		self.response.headers.append(("Set-Cookie", value))

	def clear_cookie(self, name, path="/", domain=None):
		self.set_cookie(name, value="", path=path, domain=domain)

	def redirect(self, url):
		newloc = urlparse.urljoin(self.request.path, url)
		if url.startswith('/'):
			newloc = self.request.host + newloc

		self.response.status = "303 See Other"
		self.response.headers = {'Content-Type': 'text/html', 'Location': newloc}
	
	def cleanup(self):
		self.request.clear()
		self.response.clear()
