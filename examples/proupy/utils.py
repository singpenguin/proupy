#!/usr/bin/env python
# encoding:utf-8

class Storage(dict):
	"""
	A Storage object is like a dictionary except `obj.foo` can be used
	in addition to `obj['foo']`.

		>>> o = storage(a=1)
		>>> o.a
		1
		>>> o['a']
		1
		>>> o.a = 2
		>>> o['a']
		2
		>>> del o.a
		>>> o.a
		Traceback (most recent call last):
			...
		AttributeError: 'a'
	"""
	def __getattr__(self, key): 
		try:
			return self[key]
		except KeyError, k:
			raise AttributeError, k

	def __setattr__(self, key, value): 
		self[key] = value

	def __delattr__(self, key):
		try:
			del self[key]
		except KeyError, k:
			raise AttributeError, k

	def __repr__(self):     
		return '<Storage ' + dict.__repr__(self) + '>'
storage = Storage

def safestr(obj, encoding='utf-8'):
	if isinstance(obj, unicode):
		return obj.encode(encoding)
	elif isinstance(obj, str):
		return obj
	else:
		return str(obj)

def htmlquote(text):
	r"""
	Encodes `text` for raw use in HTML.

		>>> htmlquote(u"<'&\">")
		u'&lt;&#39;&amp;&quot;&gt;'
	"""
	text = text.replace(u"&", u"&amp;") # Must be done first!
	text = text.replace(u"<", u"&lt;")
	text = text.replace(u">", u"&gt;")
	text = text.replace(u"'", u"&#39;")
	text = text.replace(u'"', u"&quot;")
	return text

def htmlunquote(text):
	r"""
	Decodes `text` that's HTML quoted.

		>>> htmlunquote(u'&lt;&#39;&amp;&quot;&gt;')
		u'<\'&">'
	"""
	text = text.replace(u"&quot;", u'"')
	text = text.replace(u"&#39;", u"'")
	text = text.replace(u"&gt;", u">")
	text = text.replace(u"&lt;", u"<")
	text = text.replace(u"&amp;", u"&") # Must be done last!
	return text

def websafe(val):
	r"""Converts `val` so that it is safe for use in Unicode HTML.

		>>> websafe("<'&\">")
		u'&lt;&#39;&amp;&quot;&gt;'
		>>> websafe(None)
		u''
		>>> websafe(u'\u203d')
		u'\u203d'
		>>> websafe('\xe2\x80\xbd')
		u'\u203d'
	"""
	if val is None:
		return u''
	elif isinstance(val, str):
		val = val.decode('utf-8')
	elif not isinstance(val, unicode):
		val = unicode(val)
	return htmlquote(val)

def safeunicode(obj, encoding='utf-8'):
	r"""
	Converts any given object to unicode string.
	
		>>> safeunicode('hello')
		u'hello'
		>>> safeunicode(2)
		u'2'
		>>> safeunicode('\xe1\x88\xb4')
		u'\u1234'
	"""
	t = type(obj)
	if t is unicode:
		return obj
	elif t is str:
		return obj.decode(encoding)
	elif t in [int, float, bool]:
		return unicode(obj)
	elif hasattr(obj, '__unicode__') or isinstance(obj, unicode):
		return unicode(obj)
	else:
		return str(obj).decode(encoding)
