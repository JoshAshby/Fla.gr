#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

User profile controller. Everything under the /profile
        URL is fleshed out, or linked to from here.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from seshat.route import route

from flagr.objects.publicObject import publicObject
import flagr.models.flagModel as fm
import flagr.models.labelModel as lm
import flagr.config.flagrConfig as fc
import flagr.views.pyStrap.pyStrap as ps

import models.profileModel as profilem


@route("/people/(.*)/labels")
class userViewLabels(publicObject):
        def GET(self):
                content = ""
                user = profilem.findUser(self.members[0])
                if user:
                        self.view["title"] = user["username"] + "'s' labels"

                        tabs = "<li>" + ps.baseAnchor(ps.baseIcon("user"), link="%s/people/%s" % (c.baseURL, user.username),
                                        rel="tooltip",
                                        data=[("original-title", "%s's Profile"%user.username),
                                                ("placement", "bottom")]) + "</li>"
                        tabs += "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link="%s/people/%s/flags" % (c.baseURL, user.username),
                                        rel="tooltip",
                                        data=[("original-title", "%s's Flags"%user.username),
                                                ("placement", "bottom")]) + "</li>"
                        tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("tags"), link="%s/people/%s/labels" % (c.baseURL, user.username),
                                        rel="tooltip",
                                        data=[("original-title", "%s's Labels"%user.username),
                                                ("placement", "bottom")]) + "</li>"

                        pageHead = ps.baseRow([
                                ps.baseColumn(ps.baseHeading("%s %s" % (ps.baseIcon("tags"), user["username"]), size=2), width=5),
                                ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                                ])
                        labels = lm.labelList(user.id)
                        if not labels:
                                labels = "They have no labels yet!"

                        content += ps.baseRow(ps.baseColumn(labels))

                        self.view.body = pageHead + content
                else:
                        self.view.body = """Oh no, we can't find that person in our system, are you sure that is their correct username?"""


@route("/people/(.*)/flags")
class userViewFlags(publicObject):
        def GET(self):
                start = int(self.members["start"]) if self.members.has_key("start") else 0

                user = profilem.findUser(self.members[0])
                flags = fm.flagList(user.id, True)

                nextClass = ""
                prevClass = ""

                if start == 0:
                        prevClass = "disabled"
                        prevLink = "#"
                elif start == 10:
                        prevLink = c.baseURL+"/flags"
                else:
                        prevLink = c.baseURL+"/flags?start=" + str(start-10)

                if len(flags[start+10:start+20]) <= 0:
                        nextClass = "disabled"
                        nextLink = "#"
                else:
                        nextLink = c.baseURL+"/flags?start=" + str(start+10)

                flags = flags[start:start+10]

                pager = """<ul class="pager">
        <li class="previous %s">
                <a href="%s">&larr; Previous</a>
        </li>
        <li class="next %s">
                <a href="%s">Next &rarr;</a>
        </li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)
                content = ""
                self.view["title"] = user["username"] + "'s 'flags"

                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("user"), link="%s/people/%s" % (c.baseURL, user.username),
                                rel="tooltip",
                                data=[("original-title", "%s's Profile"%user.username),
                                        ("placement", "bottom")]) + "</li>"
                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("flag"), link="%s/people/%s/flags" % (c.baseURL, user.username),
                                rel="tooltip",
                                data=[("original-title", "%s's Flags"%user.username),
                                        ("placement", "bottom")]) + "</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("tags"), link="%s/people/%s/labels" % (c.baseURL, user.username),
                                rel="tooltip",
                                data=[("original-title", "%s's Labels"%user.username),
                                        ("placement", "bottom")]) + "</li>"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s %s" % (ps.baseIcon("flag"), user["username"]), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                buildMessage = "Uh oh! Looks like they don't have any flags at the moment."

                if flags:
                        flagList = fc.flagThumbnails(flags)
                else:
                        flagList = buildMessage

                content += ps.baseRow(ps.baseColumn(flagList, id="flags"))


                self.view.body = pageHead + content + pager


@route("/people/(.*)")
class userView(publicObject):
        def GET(self):
                user = profilem.findUser(self.members[0])
                self.view["title"] = user["username"]

                if user["visibility"]:
                        about = user["about"] or "They have nothing here yet!"


                        tabs = "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("user"), link="%s/people/%s" % (c.baseURL, user.username),
                                        rel="tooltip",
                                        data=[("original-title", "%s's Profile"%user.username),
                                        ("placement", "bottom")]) + "</li>"
                        tabs += "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link="%s/people/%s/flags" % (c.baseURL, user.username),
                                        rel="tooltip",
                                        data=[("original-title", "%s's Flags"%user.username),
                                        ("placement", "bottom")]) + "</li>"
                        tabs += "<li>" + ps.baseAnchor(ps.baseIcon("tags"), link="%s/people/%s/labels" % (c.baseURL, user.username),
                                        rel="tooltip",
                                        data=[("original-title", "%s's Labels"%user.username),
                                        ("placement", "bottom")]) + "</li>"

                        pageHead = ps.baseRow([
                                ps.baseColumn(ps.baseHeading("%s %s" % (ps.baseIcon("user"), user["username"]), size=2), width=5),
                                ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                                ])

                        if user["emailVisibility"]:
                                email = user["email"]
                        else:
                                email = "Hidden"

                        content = ps.baseRow([
                                        ps.baseColumn(
                                                ps.baseWell(
                                                        ps.baseColumn(ps.baseBold("Email: ", classes="muted")) +
                                                        ps.baseColumn(email)
                                                        ),
                                                width=10
                                                )
                                        ])

                        content += ps.baseRow(ps.baseColumn(about))

                        self.view.body = pageHead + content

                else:
                        self.view.body = ps.baseHeading("How sad!", size=2) + ps.baseParagraph("%s's profile isn't publically visible!"%user["username"])
