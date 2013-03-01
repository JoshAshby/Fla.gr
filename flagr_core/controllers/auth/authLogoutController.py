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

import models.user.userModel as um

@route("/auth/logout")
class logout(baseHTMLObject):
    def GET(self):
        """
        Simply log the user out. Nothing much to do here.

        redirect to login page after we're done.
        """
        um.logout(self.session)

        self.head = ("303 SEE OTHER", [("location", ("/auth/login"))])


