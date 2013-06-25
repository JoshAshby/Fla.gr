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
import traceback


class baseHTTPObject(object):
        __level__ = 0
        __login__ = False

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

        def build(self, data, reply):
            error = False
            content = ""

            if not error and self.__level__:
                if self.session.level == 100:
                    """
                    Duh, This user is obviously omnicious and has access to every
                    area in the site.
                    """
                    pass

                elif self.__level__ > self.request.session.level:
                    loc = "/"
                    if self.request.session.loggedIn:
                        loc = "/your/flags"
                    self.request.session.pushAlert("You don't have the rights to access this.")
                    self.head = ("303 SEE OTHER", [("location", loc)])
                    error = True

            elif self.__login__ and not self.request.session.loggedIn:
                    self.request.session.pushAlert("You need to be logged in to view this page.")
                    self.head = ("303 SEE OTHER", [("location", "/auth/login")])
                    error = True

            if not error:
                try:
                    content = getattr(self, self.request.method)() or ""
                    content = unicode(content)
                except:
                    content = traceback.format_exc()
                    error = True

            if self.head[0] != "303 SEE OTHER":
                del self.request.session.alerts

            data.put(content)
            data.put(StopIteration)

            reply.put(self.head)
            reply.put(StopIteration)

            if error:
                raise Exception("Controller failed to finish...")

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
