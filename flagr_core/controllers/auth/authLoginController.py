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
from utils.baseHTMLObject import baseHTMLObject

from views.auth.authLoginTmpl import authLoginTmpl

import models.user.userModel as um


@route("/auth/login")
class authLogin(baseHTMLObject):
    """

    """
    __name__ = "login"
    def GET(self):
        """
        Display the login page or redirect to their dashboard if they are already logged in
        """
        if self.session.loggedIn:
            self.head = ("303 SEE OTHER",
                [("location", "/your/dashboard")])
            self.session.pushAlert("Hey look, you're already signed in!")

        else:
            loginForm = authLoginTmpl(searchList=[self.tmplSearchList])
            return loginForm

    def POST(self):
        """
        Use form data to check login, and the redirect if successful
        if not successful then redirect to the login page again.
        """
        passwd = self.env["members"]["password"]
        name = self.env["members"]["username"]

        try:
            um.userORM.login(name, passwd, self.env["cookie"])
            self.head = ("303 SEE OTHER", [("location", "/your/dashboard")])
            self.session.pushAlert("Welcome back, %s!" % name)

        except Exception as exc:
            self.head = ("303 SEE OTHER", [("location", "/auth/login")])
            self.session.pushAlert("Something went wrong:<br>%s Please try again." % exc)
