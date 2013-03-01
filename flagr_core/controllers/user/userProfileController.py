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

            tabs = fc.tabs([
                {"title": "%s's Profile" % user.username,
                    "link": c.baseURL+"/people/%s" % user.username,
                    "icon": "user"},
                {"title": "%s's Flags" % user.username,
                    "link": c.baseURL+"/people/%s/flags" % user.username,
                    "icon": "flag"},
                {"active": True,
                    "title": "%s's Labels" % user.username,
                    "link": c.baseURL+"/people/%s/labels" % user.username,
                    "icon": "tags"},
                ])

            pageHead = ps.baseRow([
                ps.baseColumn(
                    ps.baseHeading("%s %s" % (ps.baseIcon("tags"),
                        user["username"]),
                    size=2),
                width=5),
                ps.baseColumn(tabs, width=5)
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
        user = profilem.findUser(self.members[0])
        flags = fm.flagList(user.id, True)

        flags, pager = fc.listPager(flags,
            c.baseURL+"/people/%"%user.username,
            self.members)

        content = ""
        self.view["title"] = user["username"] + "'s 'flags"

        tabs = fc.tabs([
            {"title": "%s's Profile" % user.username,
                "link": c.baseURL+"/people/%s" % user.username,
                "icon": "user"},
            {"active": True,
                "title": "%s's Flags" % user.username,
                "link": c.baseURL+"/people/%s/flags" % user.username,
                "icon": "flag"},
            {"title": "%s's Labels" % user.username,
                "link": c.baseURL+"/people/%s/labels" % user.username,
                "icon": "tags"},
            ])

        pageHead = ps.baseRow([
            ps.baseColumn(ps.baseHeading("%s %s" % (ps.baseIcon("flag"), user["username"]), size=2), width=5),
            ps.baseColumn(tabs, width=5)
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

            tabs = fc.tabs([
                {"active": True,
                    "title": "%s's Profile" % user.username,
                    "link": c.baseURL+"/people/%s" % user.username,
                    "icon": "user"},
                {"title": "%s's Flags" % user.username,
                    "link": c.baseURL+"/people/%s/flags" % user.username,
                    "icon": "flag"},
                {"title": "%s's Labels" % user.username,
                    "link": c.baseURL+"/people/%s/labels" % user.username,
                    "icon": "tags"},
                ])

            pageHead = ps.baseRow([
                ps.baseColumn(
                    ps.baseHeading("%s %s" % (ps.baseIcon("user"),
                        user["username"]),
                    size=2),
                width=5),
                ps.baseColumn(tabs, width=5)
                ])

            if user["emailVisibility"]:
                email = user["email"]
            else:
                email = "Hidden"

            content = ps.baseRow([
                ps.baseColumn(
                    ps.baseWell(
                        ps.baseColumn(ps.baseBold("Email: ",
                            classes="muted")) +
                        ps.baseColumn(email)
                        ),
                    width=10
                    )
                ])

            content += ps.baseRow(ps.baseColumn(about))

            self.view.body = pageHead + content
        else:
            self.view.body = ps.baseHeading("How sad!", size=2)
            self.view.body += ps.baseParagraph("%s's profile isn't publically visible!"%user["username"])
