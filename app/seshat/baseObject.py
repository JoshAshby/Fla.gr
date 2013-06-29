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


class baseHTTPObject(object):
        __level__ = 0
        __login__ = False
        __admin__ = False

        """
        Base HTTP page response object
        This determins which REQUEST method to send to,
        along with authentication level needed to access the object.
        """
        def __init__(self, request):
            self.request = request
            self.finishInit()

        def finishInit(self):
            pass

        def build(self):
            error = False
            content = ""

            if self.__admin__:
                if self.request.session.hasAdmin:
                    """
                    Duh, This user is obviously omnicious and has access to every
                    area in the site.
                    """
                    pass

                elif self.request.session.userID:
                    loc = "/you"
                    self.request.session.pushAlert("You don't have the rights to access this.", level="error")
                    self.head = ("303 SEE OTHER", [("location", loc)])
                    error = True
                else:
                    loc = "/"
                    self.request.session.pushAlert("You need to be logged in as an Admin", level="error")
                    self.head = ("303 SEE OTHER", [("location", loc)])
                    error = True

            elif self.__login__ and not self.request.session.userID:
                self.request.session.pushAlert("You need to be logged in to view this page.", level="error")
                self.head = ("303 SEE OTHER", [("location", "/auth/login")])
                error = True

            if not error:
                self.noErrorHook()
                content = getattr(self, self.request.method)() or ""
                content = self.postMethod(content)
                if content: content = unicode(content)
            else:
                self.errorHook()

            if self.head[0] != "303 SEE OTHER":
                del self.request.session.alerts

            return content, self.head

        def noErrorHook(self):
            pass

        def errorHook(self):
            pass

        def postMethod(self, content):
            return content

        def _404(self):
            self.head = ("404 NOT FOUND", [])

        def HEAD(self):
            """
            This is wrong since it should only return the headers... technically...
            """
            return self.GET()

        def GET(self):
            pass

        def POST(self):
            pass

        def PUT(self):
            pass

        def DELETE(self):
            pass
