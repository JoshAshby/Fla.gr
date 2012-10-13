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
import models.profileModel as youm
import flagr.flagrConfig as fc

from objects.profileObject import profileObject as profilePage
from objects.publicProfileObject import publicProfileObject as publicProfilePage
from seshat.route import route

import views.pyStrap.pyStrap as ps


@route("/you")
@route("/profile")
class userIndex(profilePage):
        def GET(self):
                self.view["title"] = "You!"

                new = ps.baseSplitDropdown(btn=ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                        classes="btn-info", link=c.baseURL+"/flags/new"),
                        dropdown=ps.baseMenu(name="flagDropdown",
                                items=[{"name": "%s Note" % ps.baseIcon("list-alt"), "link": c.baseURL+"/flags/new/note"},
                                        {"name": "%s Bookmark" % ps.baseIcon("bookmark"), "link": c.baseURL+"/flags/new/bookmark"}]
                                ),
                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                classes="dropdown-toggle btn-info",
                                data=[("toggle", "dropdown"),
                                        ("original-title", "Quick select")],
                                rel="tooltip"))

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s You! (%s)" % (ps.baseIcon("user"), c.session.user.username), size=1)),
                                ps.baseButtonToolbar([
                                        new,
                                        ps.baseButtonGroup([
                                                ps.baseAButton(ps.baseIcon("cogs"),
                                                        link=c.baseURL+"/your/settings",
                                                        rel="tooltip",
                                                        data=[("original-title", "Your settings")])
                                                ]),
                                ], classes="pull-right")
                        ]) + "<hr>"

                email = " joshuaashby@joshashby.com"
                #email = " %s"%c.session.user.email if c.session.user["email"] else "You don't have an email registered!"

                #if not c.session.user["emailVisibility"]:
                if not True:
                        emailVis = ps.baseLabel("%s Private" % ps.baseIcon("eye-close"))
                else:
                        emailVis = ps.baseLabel("%s Public" % ps.baseIcon("globe"))


                #if not c.session.user["visibility"]:
                if not True:
                        vis = ps.baseLabel("%s Private" % ps.baseIcon("eye-close"))
                else:
                        vis = ps.baseLabel("%s Public" % ps.baseIcon("globe"))

                content = ps.baseRow([
                                ps.baseColumn(
                                        ps.baseWell(
                                                ps.baseColumn(ps.baseBold("Profile: ", classes="muted")) +
                                                ps.baseColumn(vis) +
                                                ps.baseColumn(ps.baseBold("Email: ", classes="muted")) +
                                                ps.baseColumn(emailVis + email)
                                                ),
                                        width=8
                                        )
                                ])

                labels = lm.labelList(c.session.userID)
                if not labels:
                        labels = "You have no labels yet!"

                content += ps.baseRow([ps.baseColumn(ps.baseBold(ps.baseIcon("tags")+" Your labels:", classes="muted")), ps.baseColumn(lm.labelList(c.session.userID))]) + "<hr>"

                flags = fm.flagList(c.session.userID, True)
                buildMessage = "Uh oh! Looks like you don't have any flags at the moment, why don't you make one with the new flag button at the top of this page?"

                if flags:
                        flagList = fc.flagThumbnails(flags[:10], 8)
                        flagList = ps.baseUL(flagList, classes="thumbnails") + ps.baseAButton("See all your flags",
                                        link=c.baseURL+"/your/flags")
                else:
                        flagList = buildMessage

                content += ps.baseRow(ps.baseColumn(flagList, id="flags"))


                self.view.body = pageHead + content
                self.view.scripts = ps.baseScript("""
                        $('.btn-group').tooltip({
                              selector: "a[rel=tooltip]"
                        })
                """)

@route("/you/edit")
@route("/your/settings")
@route("/profile/edit")
class userEdit(profilePage):
        def GET(self):
                pass

        def POST(self):
                pass


@route("/profile/(.*)")
@route("/profile/(.*)/view")
@route("/peep/(.*)")
@route("/person/(.*)")
class userView(publicProfilePage):
        def GET(self):
                pass

        def POST(self):
                pass
