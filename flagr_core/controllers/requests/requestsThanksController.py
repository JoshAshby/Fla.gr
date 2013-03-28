#!/usr/bin/env python
"""
fla.gr controller for displaying a thank you page after requesting an invite
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.requests.requestsThanksTmpl import requestsThanksTmpl


@route("/request/thanks")
class requestThanks(baseHTMLObject):
    __name__ = "thanks!"
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            view = requestsThanksTmpl(searchList=[self.tmplSearchList])
            return view
        else:
            self.head = ("404 NOT FOUND", [])
