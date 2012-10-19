#!/usr/bin/env python2
"""
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
import views.smartPage as sp
import models.blocks.helpers as helpers


class baseHTTPPageObject(object):
        __level__ = None
        __login__ = "False"
        __menu__ = ""
        """
        Base HTTP page response object
        This determins which REQUEST method to send to,
        along with authentication level needed to access the object.
        """
        def __init__(self, env, members):
                self.env = env
                self.members = members

                self.view = sp.flagrPage()

                self.method = env["REQUEST_METHOD"]

                self.head = ("200 OK", 
                        [
                                ("Content-type", "text/html"),
                        ])

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
                                c.session.pushMessage("You need to have %s rights to access this." % self.__level__)
                                self.head = ("303 SEE OTHER", [("location", "/you")])
                                error = True

                elif helpers.boolean(self.__login__) and not helpers.boolean(c.session.loggedIn):
                        c.session.pushMessage("You need to be logged in to view this.")
                        self.head = ("303 SEE OTHER", [("location", "/auth/login")])
                        error = True

                if not error:
                        getattr(self, self.method)()
                        if not self.view.title: self.view.title = self.__menu__
                        self.view.title = "%s - %s" % (c.appName, self.view.title)
                        self.view.scripts += """
                        <script>
                        $('.btn-group').tooltip({
                                selector: "a[rel=tooltip]"
                                })
                        $('.nav-tabs').tooltip({
                                selector: "a[rel=tooltip]"
                                })
                        </script>
                        """
                        self.view.build()
                        content = self.view
                        if self.method == "GET" or self.method == "HEAD":
                                c.session.messages = ""

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
