#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import baseView as bv
import models.blocks.helpers as helpers


class baseHTTPObject(object):
        __level__ = None
        __login__ = "False"
        __menu__ = ""
        head = ("200 OK", 
                [
                        ("Content-type", "text/html"),
                ])
        view = bv.baseView()

        """
        Base HTTP page response object
        This determins which REQUEST method to send to,
        along with authentication level needed to access the object.
        """
        def __init__(self, env, members):
                self.env = env
                self.members = members

                self.method = env["REQUEST_METHOD"]

                self.finishInit()

        def finishInit(self):
                pass

        def build(self, data, reply):
                error = False

                if c.session.redirect == "True":
                        self.head = ("303 SEE OTHER", [("location", c.session.history)])
                        c.session.redirect = ""
                        error = True

                content = ""

                matches = c.authRegex.findall(str(self.__class__.__name__))
                if not error and self.__level__:
                        if c.session.user["level"] == "GOD":
                                """
                                Duh, This user is obviously omnicious and has access to every
                                area in the site.
                                """
                                pass

                        elif self.__level__ != c.session.user["level"]:
                                c.session.pushAlert("You need to have %s rights to access this." % self.__level__)
                                self.head = ("303 SEE OTHER", [("location", "/")])
                                error = True

                elif helpers.boolean(self.__login__) and not helpers.boolean(c.session.loggedIn):
                        c.session.pushAlert("You need to be logged in to view this.")
                        self.head = ("303 SEE OTHER", [("location", "/")])
                        error = True

                if not error:
                        getattr(self, self.method)()
                        if not self.view.title: self.view.title = self.__menu__
                        self.view.title = "%s - %s" % (c.appName, self.view.title)
                        self.view.scripts += ""
                        self.view.css += ""
                        content = self.view.build()
                        if self.method == "GET" or self.method == "HEAD":
                                c.session.alerts = ""

                data.put(str(content))
                data.put(StopIteration)

                reply.put(self.head)
                reply.put(StopIteration)

        def HEAD(self):
                return self.GET()

        def GET(self):
                pass

        def POST(self):
                pass

        def PUT(self):
                pass

        def DELETE(self):
                pass
