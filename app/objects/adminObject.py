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


class adminObject(bo.baseHTTPPageObject):
       __level__ = "admin"
       __login__ = "True"
       __name__ = "admin"
       def finishInit(self):
               self.view.sidebar = ps.baseWell(ps.baseNavList(items=[{"header": "Things to do..."}, 
                {"link": c.baseURL + "/admin/posts", "name": "%s Edit Front Page Posts"%ps.baseIcon("edit")},
                {"link": c.baseURL + "/admin/users", "name": "%s Manage Some Users" % ps.baseIcon("user")}]))
