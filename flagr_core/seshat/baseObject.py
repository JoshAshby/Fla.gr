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
import models.basic.sessionModel as sm
import traceback

class baseHTTPObject(object):
        __level__ = 0
        __login__ = False

        """
        Base HTTP page response object
        This determins which REQUEST method to send to,
        along with authentication level needed to access the object.
        """
        def __init__(self, env, members, sessionID):
                self.env = {"env": env, "members": members, "method": env["REQUEST_METHOD"], "cookie": sessionID}
                self.session = sm.session(sessionID)

                self.finishInit()

        def finishInit(self):
                pass

        def build(self, data, reply):
                error = False

                if self.session.redirect:
                        self.head = ("303 SEE OTHER", [("location", self.session.history)])
                        self.session.redirect = False
                        self.session.pushAlert("You've been redirected to " + str(self.session.history))
                        error = True

                content = ""

                if not error and self.__level__:
                    if self.session.level == 100:
                        """
                        Duh, This user is obviously omnicious and has access to every
                        area in the site.
                        """
                        pass

                    elif self.__level__ > self.session.level:
                        loc = "/"
                        if self.session.loggedIn:
                            loc = "/your/flags"
                        self.session.pushAlert("You don't have the rights to access this.")
                        self.head = ("303 SEE OTHER", [("location", loc)])
                        error = True

                elif self.__login__ and not self.session.loggedIn:
                        self.session.pushAlert("You need to be logged in to view this page.")
                        self.head = ("303 SEE OTHER", [("location", "/auth/login")])
                        error = True

                if not error:
                    try:
                        content = getattr(self, self.env["method"])() or ""
                        content = str(content)
                    except:
                        content = traceback.format_exc()
                        error = True

                if self.head[0] != "303 SEE OTHER":
                    del self.session.alerts
                self.session.saveAlerts()

                data.put(content)
                data.put(StopIteration)

                reply.put(self.head)
                reply.put(StopIteration)

                if error:
                    raise Exception("Controller failed to finish...")

        def _404(self):
            self.head = ("404 NOT FOUND", [])

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

