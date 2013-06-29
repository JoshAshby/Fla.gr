#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.baseObject import baseHTTPObject
from views.template import template


class baseHTMLObject(baseHTTPObject):
    def finishInit(self):
        self.head = ("200 OK", [("Content-Type", "text/html")])

        try:
            title = self._title
        except:
            title = "untitledFlagrPage"

        self.request.title = title

    def noErrorHook(self):
        try:
          tmpl = self._defaultTmpl
          self.view = template(tmpl, self.request)
        except:
          self.view = ""

    def postMethod(self, content):
        if type(content) == template:
            return content.render()
        else:
            return content
