#!/usr/bin/env python
# coding: utf-8

import os, sys

#path = os.path.dirname(os.path.realpath(__file__))
#sys.path.append(path)
#os.chdir(path)
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
#os.chdir(abspath)

import web
from config.url import urls

app = web.application(urls, globals(), autoreload=True)


if __name__ == "__main__":
	#web.wsgi.runwsgi=lambda func,addr=None: web.wsgi.runfcgi(func,addr)
	app.run()
