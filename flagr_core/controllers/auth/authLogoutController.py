#!/usr/bin/env python2
"""
fla.gr controller for authentication logout
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject


@route("/auth/logout")
class authLogout(baseHTMLObject):
    def GET(self):
        """
        Simply log the user out. Nothing much to do here.

        redirect to login page after we're done.
        """
        if self.session.logout():
            self.session.pushAlert("Come back soon!", "B'ahBye...", "info")

        self.head = ("303 SEE OTHER", [("location", ("/auth/login"))])


