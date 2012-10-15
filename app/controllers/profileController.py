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

import flagr.models.flagModel as fm
import flagr.models.labelModel as lm
import models.profileModel as profilem
import flagr.flagrConfig as fc

from objects.publicProfileObject import publicProfileObject as publicProfilePage
from seshat.route import route

import views.pyStrap.pyStrap as ps


@route("/people/(.*)/labels")
class userView(publicProfilePage):
        def GET(self):
                content = ""
                user = profilem.findUser(self.members[0])
                self.view["title"] = user["username"] + "'s' labels"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s %s's labels" % (ps.baseIcon("user"), user["username"]), size=1)),
                        ]) + "<hr>"

                labels = lm.labelList(user.id)
                if not labels:
                        labels = "They have no labels yet!"

                content += ps.baseRow(ps.baseColumn(labels)) + "<hr>"

                self.view.body = pageHead + content
                self.view.scripts = ps.baseScript("""
                        $('.btn-group').tooltip({
                              selector: "a[rel=tooltip]"
                        })
                """)



@route("/people/(.*)/flags")
class userView(publicProfilePage):
        def GET(self):
                content = ""
                user = profilem.findUser(self.members[0])
                self.view["title"] = user["username"] + "'s 'flags"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s %s's flags" % (ps.baseIcon("user"), user["username"]), size=1)),
                        ]) + "<hr>"

                flags = fm.flagList(c.session.userID, True)
                buildMessage = "Uh oh! Looks like they don't have any flags at the moment."

                if flags:
                        flagList = fc.flagThumbnails(flags, 10)
                else:
                        flagList = buildMessage

                content += ps.baseRow(ps.baseColumn(flagList, id="flags"))


                self.view.body = pageHead + content
                self.view.scripts = ps.baseScript("""
                        $('.btn-group').tooltip({
                              selector: "a[rel=tooltip]"
                        })
                """)


@route("/people/(.*)")
class userView(publicProfilePage):
        def GET(self):
                user = profilem.findUser(self.members[0])
                self.view["title"] = user["username"]

                if user["visibility"]:
                        about = c.session.user["about"] or "They have nothing here yet!"
                        self.view.sidebar = ps.baseWell(ps.baseNavList(items=[{"header": "Their stuff"},
                                {"link": c.baseURL + "/people/%s/flags"%user["username"], "name": "%s Their flags"%ps.baseIcon("flag")},
                                {"link": c.baseURL + "/people/%s/labels"%user["username"], "name": "%s Their labels"%ps.baseIcon("tags")},
                                "divider",
                                {"header": "About %s"%user["username"]},
                                {"text": about}
                        ]))

                        pageHead = ps.baseRow([
                                ps.baseColumn(ps.baseHeading("%s %s" % (ps.baseIcon("user"), user["username"]), size=1)),
                                ]) + "<hr>"

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
                                                width=8
                                                )
                                        ])

                        labels = lm.labelList(user.id)
                        if not labels:
                                labels = "They have no labels yet!"

                        content += ps.baseRow([ps.baseColumn(ps.baseBold(ps.baseIcon("tags")+" Their labels:", classes="muted")), ps.baseColumn(labels)]) + "<hr>"

                        flags = fm.flagList(c.session.userID, True)
                        buildMessage = "Uh oh! Looks like they don't have any flags at the moment."

                        if flags:
                                flagList = fc.flagThumbnails(flags[:10], 8)
                                flagList = flagList + ps.baseAButton("See all their flags",
                                                link=c.baseURL+"/people/%s/flags"%user["username"])
                        else:
                                flagList = buildMessage

                        content += ps.baseRow(ps.baseColumn(flagList, id="flags"))


                        self.view.body = pageHead + content
                        self.view.scripts = ps.baseScript("""
                                $('.btn-group').tooltip({
                                      selector: "a[rel=tooltip]"
                                })
                        """)

                else:
                        self.view.body = ps.baseHeading("How sad!", size=1) + ps.baseParagraph("%s's profile isn't publically visible!"%user["username"])
