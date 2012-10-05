#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
controller for authentication stuff.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from objects.baseObject import baseHTTPPageObject as basePage
from seshat.route import route

import views.pyStrap.pyStrap as ps


@route("/auth/login")
class login(basePage):
        __menu__ = "Login"
        def GET(self):
                """
                Display the login page.
                """
                if c.session.loggedIn == "True":
                        self.head = ("303 SEE OTHER", [("location", "/")])
                        c.session.pushMessage("Hey look, you're already signed in!")

                else:
                        loginForm = ps.baseHeading("Please Login...", size=2) + ps.baseHorizontalForm(action=c.baseURL+"/auth/login",
                                method="POST",
                                fields=[
                                {"label": "Username: ", "content": ps.baseInput(type="text", name="username", placeholder="Username")},
                                {"label": "Password: ", "content": ps.baseInput(type="password", name="password", placeholder="Password")}],
                                actions = [ps.baseSubmit("Login")])

                        self.view["body"] = loginForm

        def POST(self):
                """
                Use form data to check login, and the redirect if successful
                if not redirect to login page again.
                """
                passwd = self.members["password"]
                name = self.members["username"]

                try:
                        c.session.login(name, passwd)
                        self.head = ("303 SEE OTHER", [("location", "/flags")])
                        c.session.pushMessage("Welcome back, %s!" % name, icon="")

                except Exception as exc:
                        self.head = ("303 SEE OTHER", [("location", "/auth/login")])
                        c.session.pushMessage("Something went wrong:<br>%s Please try again." % exc, type="error", title="Oh no!", icon="fire")


@route("/auth/logout")
class logout(basePage):
        def GET(self):
                """
                Simply log the user out. Nothing much to do here.

                redirect to login page after we're done.
                """
                c.session.logout()

                self.head = ("303 SEE OTHER", [("location", ("/auth/login"))])
                c.session.pushMessage("See you again, next time!", icon="")
