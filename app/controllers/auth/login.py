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
from seshat.baseObject import HTMLObject
import models.modelExceptions.sessionExceptions as se


@autoRoute()
class login(HTMLObject):
    """

    """
    _title = "login"
    _defaultTmpl = "public/auth/login"
    def GET(self):
        """
        Display the login page or redirect to their dashboard if they are already logged in
        """
        if self.request.session.userID:
            self.head = ("303 SEE OTHER",
                [("location", "/you")])
            self.request.session.pushAlert("It looks like you're already signed in!", "Hey there!", "info")

        else:
            return self.view

    def POST(self):
        """
        Use form data to check login, and the redirect if successful
        if not successful then redirect to the login page again.
        """
        passwd = self.request.getParam("password")
        name = self.request.getParam("username")

        if not passwd and not name:
            return self.view

        exc = ""
        try:
            self.request.session.login(name, passwd)
            self.head = ("303 SEE OTHER", [("location", "/you")])
            self.request.session.pushAlert("Welcome back, %s!" % name, "Ohia!", "success")
            return

        except se.usernameError as e:
            exc = e
            self.view.data = {"usernameError": True}
        except se.passwordError as e:
            exc = e
            self.view.data = {"username": name}
            self.view.data = {"passwordError": True}
        except se.banError as e:
            exc = e

        exc = unicode(exc).strip("'")

        self.request.session.pushAlert("%s <br/>Please try again." % exc, "Uh oh...", "error")
        return self.view
