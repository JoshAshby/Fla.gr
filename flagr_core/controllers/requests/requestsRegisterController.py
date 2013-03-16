#!/usr/bin/env python2
"""
fla.gr controller for registering after having an invite accepted

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.requests.requestsRegisterTmpl import requestsRegisterTmpl


@route("/request/register")
class requestsRegister(baseHTMLObject):
    __name__ = "register"
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            view = requestsRegisterTmpl(searchList=[self.tmplSearchList])
            return view
        else:
            self.head = ("404 NOT FOUND", [])
