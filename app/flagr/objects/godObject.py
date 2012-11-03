#!/usr/bin/env python
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


class godObject(bo.baseHTTPObject):
    __level__ = "GOD"
    __login__ = True
    __name__ = "god"
    view = fv.flagrView
    def finishInit(self):
        self.view.sidebar = ps.baseWell(
            ps.baseNavList(
                items=[
                    {"header": "Your Throne Awaits..."},
                    {"link": c.baseURL + "/god",
                        "name": "%s Front Panel"%ps.baseIcon("dashboard")},
                    {"link": c.baseURL + "/god/flags",
                        "name": "%s All the Flags"%ps.baseIcon("flag")},
                    {"link": c.baseURL + "/god/search/reindex",
                        "name": "%s Reindex Search" % ps.baseIcon("magic")}
                ]
            )
        )
