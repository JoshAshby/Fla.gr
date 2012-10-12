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
import objects.baseObject as bo
import views.pyStrap.pyStrap as ps


class flagrObject(bo.baseHTTPPageObject):
       __name__ = "flagr"
       def finishInit(self):
               """
               if c.session.loggedIn:
                       self.view.sidebar = ps.baseWell(
                                ps.baseNavList(items=[
                                        {"header": "Welcome to fla.gr!"}, 
                                        {"link": c.baseURL + "/flags/new", "name": "%s Make a new Flag"%ps.baseIcon("plus-sign")}
                                        ])
                                )
                """
