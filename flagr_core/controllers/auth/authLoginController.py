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
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.auth.authLoginTmpl import authLoginTmpl

import models.user.userModel as um
import utils.sessionExceptions as use


@autoRoute()
class authLogin(baseHTMLObject):
    """

    """
    _title = "login"
    def GET(self):
        """
        Display the login page or redirect to their dashboard if they are already logged in
        """
        if self.session.loggedIn:
            self.head = ("303 SEE OTHER",
                [("location", "/you")])
            self.session.pushAlert("It looks like you're already signed in!", "Hey there!", "info")

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
            self.head = ("303 SEE OTHER", [("location", "/you")])
            self.session.pushAlert("Welcome back, %s!" % name, "Ohia!", "success")

        except Exception as exc:
            self.session.pushAlert("%s <br/>Please try again." % exc, "Uh oh...", "error")
            loginForm = authLoginTmpl(searchList=[self.tmplSearchList])

            if type(exc) == use.usernameError:
                loginForm.usernameError = True
            elif type(exc) == use.passwordError:
                loginForm.passwordError = True
                loginForm.username = name
            elif type(exc) == use.banError:
                loginForm.banError = True

            return loginForm
