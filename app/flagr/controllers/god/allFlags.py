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

from flagr.objects.godObject import godObject
from seshat.route import route
import flagr.views.pyStrap.pyStrap as ps
import flagr.config.flagrConfig as fc
import flagr.models.flagModel as fm

import logging
logger = logging.getLogger(c.logName+".allFlags")


@route("/god/flags(.*)")
class flagsIndex_god(godObject):
    __menu__ = "Deity Flags"
    def GET(self):
        typer = self.members[0].strip("/")

        if typer == "private":
            flags = fm.flagList(deity=True, private=True)
            title = "Private Flags"
            tabs = fc.tabs([
                {"title": "All Flags",
                    "link": c.baseURL+"/god/flags",
                    "icon": "flag"},
                {"title": "Public Flags",
                    "link": c.baseURL+"/god/flags/public",
                    "icon": "globe"},
                {"active": True,
                    "title": "Private Flags",
                    "link": c.baseURL+"/god/flags/private",
                    "icon": "eye-close"},
                ])
        elif typer == "public":
            flags = fm.flagList(deity=True, public=True)
            title = "Public Flags"
            tabs = fc.tabs([
                {"title": "All Flags",
                    "link": c.baseURL+"/god/flags",
                    "icon": "flag"},
                {"active": True,
                    "title": "Public Flags",
                    "link": c.baseURL+"/god/flags/public",
                    "icon": "globe"},
                {"title": "Private Flags",
                    "link": c.baseURL+"/god/flags/private",
                    "icon": "eye-close"},
                ])
        else:
            flags = fm.flagList(deity=True)
            title = "All Flags"
            tabs = fc.tabs([
                {"active": True,
                    "title": "All Flags",
                    "link": c.baseURL+"/god/flags",
                    "icon": "flag"},
                {"title": "Public Flags",
                    "link": c.baseURL+"/god/flags/public",
                    "icon": "globe"},
                {"title": "Private Flags",
                    "link": c.baseURL+"/god/flags/private",
                    "icon": "eye-close"},
                ])


        flags, pager = fc.listPager(flags, "/god/flags", self.members)

        pageHead = ps.baseRow([
            ps.baseColumn(
                ps.baseHeading("%s %s" % (ps.baseIcon("flag"),
                        title),
                    size=2),
                width=5),
            ps.baseColumn(tabs,
                width=3)
            ])
        content = fc.flagThumbnails(flags, True)
        self.view.body = pageHead + content

        self.view.body += pager


@route("/god/flags/user")
class flagUser_god(godObject):
        def GET(self):
                pass


@route("/god/flags/user/(.*)")
class flagUser_god(godObject):
        def GET(self):
                pass
