#!/usr/bin/env python
"""
fla.gr controller for displaying a thank you page after requesting an invite

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.requests.requestsThanksTmpl import requestsThanksTmpl


@route("/request/thanks")
class requestThanks(baseHTMLObject):
    _title = "thanks!"
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            view = requestsThanksTmpl(searchList=[self.tmplSearchList])
            return view
        else:
            self.head = ("404 NOT FOUND", [])
