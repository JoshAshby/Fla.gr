#!/usr/bin/env python
"""
fla.gr main you dashboard controller

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject


@route("/you/dashboard(.*)")
@route("/your/dashboard(.*)")
class youDashboard(baseHTMLObject):
    def GET(self):
        return "hello, " + self.session.username
