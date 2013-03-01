#!/usr/bin/env python2
"""
fla.gr controller for authentication login

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from seshat.baseHTMLObject import baseHTMLObject

from views.auth.authRegisterTmpl import authRegisterTmpl

import models.request.requestModel as rm


@route("/register")
@route("/auth/register")
class register(baseHTMLObject):
    def GET(self):
        """
        """
        view = authRegisterTmpl(searchList=[self.tmplSearchList])
        return view

    def POST(self):
        """
        """
        email = self.env["members"]["email"]

        newRequest = rm.requestORM(email)
        newRequest.save()

        self.head = ("303 SEE OTHER",
            [("location", "/auth/thanks")])
