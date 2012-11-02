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
import seshat.baseObject as bo
import flagr.views.pyStrap.pyStrap as ps
import flagr.views.flagrView as fv


class adminObject(bo.baseHTTPObject):
       __level__ = "admin"
       __login__ = True
       __name__ = "admin"
       view = fv.flagrView
       def finishInit(self):
               self.view.sidebar = ps.baseWell(ps.baseNavList(items=[{"header": "Things to do..."},
                {"link": c.baseURL + "/admin", "name": "%s Front Panel"%ps.baseIcon("dashboard")},
                {"link": c.baseURL + "/admin/posts", "name": "%s Blog Posts"%ps.baseIcon("rss")},
                {"link": c.baseURL + "/admin/carousels", "name": "%s Blog Carousel"%ps.baseIcon("play")},
                {"link": c.baseURL + "/admin/users", "name": "%s Manage Users" % ps.baseIcon("group")}]))
