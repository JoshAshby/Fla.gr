#!/usr/bin/env python2
"""
fla.gr controller for requesting an invite

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.requests.requestsRequestTmpl import requestsRequestsTmpl

import models.request.requestModel as rm


@route("/request")
class requestsRequests(baseHTMLObject):
    __name__ = "request an invite"
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            view = requestsRequestsTmpl(searchList=[self.tmplSearchList])
            return view
        else:
            self.head = ("404 NOT FOUND", [])

    def POST(self):
        """
        """
        if self.snv["cfg"].enableRequests:
            email = self.env["members"]["email"] if self.env["members"].has_key("email") else ""

            if email:
                newRequest = rm.requestORM(email)
                newRequest.save()
                self.head = ("303 SEE OTHER",
                    [("location", "/request/thanks")])
            else:
                view = requestsRequestsTmpl(searchList=[self.tmplSearchList])
                view.emailError = True
                return view
