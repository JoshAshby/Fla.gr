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


@route("/god/flags")
class flagsIndex_god(godObject):
        __menu__ = "Deity Flags"
        def GET(self):
                start = int(self.members["start"]) if self.members.has_key("start") else 0

                flags = fm.flagList(deity=True)

                nextClass = ""
                prevClass = ""

                if start == 0:
                        prevClass = "disabled"
                        prevLink = "#"
                elif start == 10:
                        prevLink = c.baseURL+"/god/flags"
                else:
                        prevLink = c.baseURL+"/god/flags?start=" + str(start-10)

                if len(flags[start+10:start+20]) <= 0:
                        nextClass = "disabled"
                        nextLink = "#"
                else:
                        nextLink = c.baseURL+"/god/flags?start=" + str(start+10)

                flags = flags[start:start+10]

                pager = """<ul class="pager">
        <li class="previous %s">
                <a href="%s">&larr; Previous</a>
        </li>
        <li class="next %s">
                <a href="%s">Next &rarr;</a>
        </li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)

                tabs = "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/god/flags",
                                rel="tooltip",
                                data=[("original-title", "All Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("globe"), link=c.baseURL+"/god/flags/public",
                                rel="tooltip",
                                data=[("original-title", "Public Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("eye-close"), link=c.baseURL+"/god/flags/private",
                                rel="tooltip",
                                data=[("original-title", "Private Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("search"), link=c.baseURL+"/god/search",
                                rel="tooltip",
                                data=[("original-title", "Find a Flag"),
                                        ("placement", "bottom")]) +"</li>"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s All Flags" % (ps.baseIcon("flag")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-pills pull-right"), width=3)
                        ])
                content = fc.flagThumbnails(flags, True)
                self.view.body = pageHead + content

                self.view.body += pager



@route("/god/flags/public")
class flagsIndexPublic_god(godObject):
        __menu__ = "Deity Public Flags"
        def GET(self):
                flags = fm.deityFlagList(public=True)
                start = int(self.members["start"]) if self.members.has_key("start") else 0

                nextClass = ""
                prevClass = ""

                if start == 0:
                        prevClass = "disabled"
                        prevLink = "#"
                elif start == 10:
                        prevLink = c.baseURL+"/god/flags/public"
                else:
                        prevLink = c.baseURL+"/god/flags/public?start=" + str(start-10)

                if len(flags[start+10:start+20]) <= 0:
                        nextClass = "disabled"
                        nextLink = "#"
                else:
                        nextLink = c.baseURL+"/god/flags/public?start=" + str(start+10)

                flags = flags[start:start+10]

                pager = """<ul class="pager">
        <li class="previous %s">
                <a href="%s">&larr; Previous</a>
        </li>
        <li class="next %s">
                <a href="%s">Next &rarr;</a>
        </li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)

                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/god/flags",
                                rel="tooltip",
                                data=[("original-title", "All Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("globe"), link=c.baseURL+"/god/flags/public",
                                rel="tooltip",
                                data=[("original-title", "Public Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("eye-close"), link=c.baseURL+"/god/flags/private",
                                rel="tooltip",
                                data=[("original-title", "Private Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("search"), link=c.baseURL+"/god/search",
                                rel="tooltip",
                                data=[("original-title", "Find a Flag"),
                                        ("placement", "bottom")]) +"</li>"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s All Public Flags" % (ps.baseIcon("flag")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-pills pull-right"), width=3)
                        ])
                content = fc.deityFlagThumbnails(flags)
                self.view.body = pageHead + content + pager


@route("/god/flags/private")
class flagsIndexPrivate_god(godObject):
        __menu__ = "Deity Private Flags"
        def GET(self):
                flags = fm.deityFlagList(private=True)

                start = int(self.members["start"]) if self.members.has_key("start") else 0

                nextClass = ""
                prevClass = ""

                if start == 0:
                        prevClass = "disabled"
                        prevLink = "#"
                elif start == 10:
                        prevLink = c.baseURL+"/god/flags/private"
                else:
                        prevLink = c.baseURL+"/god/flags/private?start=" + str(start-10)

                if len(flags[start+10:start+20]) <= 0:
                        nextClass = "disabled"
                        nextLink = "#"
                else:
                        nextLink = c.baseURL+"/god/flags/private?start=" + str(start+10)

                flags = flags[start:start+10]

                pager = """<ul class="pager">
        <li class="previous %s">
                <a href="%s">&larr; Previous</a>
        </li>
        <li class="next %s">
                <a href="%s">Next &rarr;</a>
        </li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)

                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/god/flags",
                                rel="tooltip",
                                data=[("original-title", "All Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("globe"), link=c.baseURL+"/god/flags/public",
                                rel="tooltip",
                                data=[("original-title", "Public Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("eye-close"), link=c.baseURL+"/god/flags/private",
                                rel="tooltip",
                                data=[("original-title", "Private Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("search"), link=c.baseURL+"/god/search",
                                rel="tooltip",
                                data=[("original-title", "Find a Flag"),
                                        ("placement", "bottom")]) +"</li>"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s All Private Flags" % (ps.baseIcon("flag")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-pills pull-right"), width=3)
                        ])
                content = fc.deityFlagThumbnails(flags)
                self.view.body = pageHead + content + pager


@route("/god/flags/user")
class flagUser_god(godObject):
        def GET(self):
                pass


@route("/god/flags/user/(.*)")
class flagUser_god(godObject):
        def GET(self):
                pass
