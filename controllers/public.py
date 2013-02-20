#!/usr/bin/env python
# coding: utf-8

import web
import mimetypes
from web import http

public_dir = "static"

def mime_type(filename):
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"

class public:
    def GET(self):
        try:
            file_name = web.ctx.path.split("/")[-1]
            web.header("Content-type", mime_type(file_name))
            return open(public_dir + web.ctx.path, "rb").read()
        except IOError:
            raise web.notfound()

            
