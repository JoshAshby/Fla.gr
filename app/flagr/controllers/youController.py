#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

You controller. Everything under the /you
        URL is handled and fleshed out, or linked to
        from here.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from seshat.route import route

import flagr.models.flagModel as fm
import flagr.models.labelModel as lm
from flagr.objects.profileObject import profileObject
import flagr.views.pyStrap.pyStrap as ps
import flagr.config.flagrConfig as fc

import models.profileModel as profilem

import bcrypt



@route("/your/flags")
class flagIndex(profileObject):
        def GET(self):
                """
                """
                self.view.tabbar = True
                self.view["title"] = "Your Flags"

                new = ps.baseSplitDropdown(btn=ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                        classes="btn-info", link=c.baseURL+"/flags/new"),
                        dropdown=ps.baseMenu(name="flagDropdown",
                                items=[{"name": "%s Note" % ps.baseIcon("list-alt"), "link": c.baseURL+"/flags/new/note"},
                                {"name": "%s Bookmark" % ps.baseIcon("bookmark"), "link": c.baseURL+"/flags/new/bookmark"}]
                                ),
                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                classes="dropdown-toggle btn-info",
                                data=[("toggle", "dropdown"),
                                ("original-title", "Quick select"),
                                ("placement", "bottom")],
                                rel="tooltip"),
                        classes="pull-right")


                start = int(self.members["start"]) if self.members.has_key("start") else 0

                flags = fm.flagList(c.session.userID, True)

                nextClass = ""
                prevClass = ""

                if start == 0:
                        prevClass = "disabled"
                        prevLink = "#"
                elif start == 10:
                        prevLink = c.baseURL+"/your/flags"
                else:
                        prevLink = c.baseURL+"/your/flags?start=" + str(start-10)

                if len(flags[start+10:start+20]) <= 0:
                        nextClass = "disabled"
                        nextLink = "#"
                else:
                        nextLink = c.baseURL+"/your/flags?start=" + str(start+10)

                flags = flags[start:start+10]

                pager = """<ul class="pager">
        <li class="previous %s">
                <a href="%s">&larr; Previous</a>
        </li>
        <li class="next %s">
                <a href="%s">Next &rarr;</a>
        </li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)


                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("user"), link=c.baseURL+"/you",
                                rel="tooltip",
                                data=[("original-title", "Your Profile"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags",
                                rel="tooltip",
                                data=[("original-title", "Your Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("tags"), link=c.baseURL+"/your/labels",
                                rel="tooltip",
                                data=[("original-title", "Your Labels"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("cogs"), link=c.baseURL+"/your/settings",
                                rel="tooltip",
                                data=[("original-title", "Your Settings"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += new

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Your Flags" % (ps.baseIcon("flag")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                visTabs = "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags/all",
                                rel="tooltip",
                                data=[("original-title", "All Your Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li>" + ps.baseAnchor(ps.baseIcon("globe"), link=c.baseURL+"/your/flags/public",
                                rel="tooltip",
                                data=[("original-title", "Your Public Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li>" + ps.baseAnchor(ps.baseIcon("eye-close"), link=c.baseURL+"/your/flags/private",
                                rel="tooltip",
                                data=[("original-title", "Your Private Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li>" + ps.baseAnchor(ps.baseIcon("search"), link="#search",
                                rel="tooltip",
                                data=[("original-title", "Search Your"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs =  ps.baseColumn(ps.baseUL(visTabs, classes="nav nav-pills"), width=1, classes="pull-right")

                buildMessage = "You have no flags at the moment, but if you want to add one, simply click the button up above to get started!."

                if flags:
                        flagList = fc.flagThumbnails(flags)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow([ps.baseColumn(flagList, width=10), visTabs]) + ps.baseRow(ps.baseColumn(pager, width=10))


@route("/your/flags/public")
class flagIndexPublic(profileObject):
        def GET(self):
                """
                """
                self.view.tabbar = True
                self.view["title"] = "Your Flags"

                new = ps.baseSplitDropdown(btn=ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                        classes="btn-info", link=c.baseURL+"/flags/new"),
                        dropdown=ps.baseMenu(name="flagDropdown",
                                items=[{"name": "%s Note" % ps.baseIcon("list-alt"), "link": c.baseURL+"/flags/new/note"},
                                {"name": "%s Bookmark" % ps.baseIcon("bookmark"), "link": c.baseURL+"/flags/new/bookmark"}]
                                ),
                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                classes="dropdown-toggle btn-info",
                                data=[("toggle", "dropdown"),
                                ("original-title", "Quick select"),
                                ("placement", "bottom")],
                                rel="tooltip"),
                        classes="pull-right")


                start = int(self.members["start"]) if self.members.has_key("start") else 0

                flags = fm.flagList(c.session.userID, True, public=True)

                nextClass = ""
                prevClass = ""

                if start == 0:
                        prevClass = "disabled"
                        prevLink = "#"
                elif start == 10:
                        prevLink = c.baseURL+"/your/flags/public"
                else:
                        prevLink = c.baseURL+"/your/flags/public?start=" + str(start-10)

                if len(flags[start+10:start+20]) <= 0:
                        nextClass = "disabled"
                        nextLink = "#"
                else:
                        nextLink = c.baseURL+"/your/flags/public?start=" + str(start+10)

                flags = flags[start:start+10]

                pager = """<ul class="pager">
        <li class="previous %s">
                <a href="%s">&larr; Previous</a>
        </li>
        <li class="next %s">
                <a href="%s">Next &rarr;</a>
        </li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)


                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("user"), link=c.baseURL+"/you",
                                rel="tooltip",
                                data=[("original-title", "Your Profile"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags",
                                rel="tooltip",
                                data=[("original-title", "Your Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("tags"), link=c.baseURL+"/your/labels",
                                rel="tooltip",
                                data=[("original-title", "Your Labels"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("cogs"), link=c.baseURL+"/your/settings",
                                rel="tooltip",
                                data=[("original-title", "Your Settings"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += new

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Your Flags" % (ps.baseIcon("flag")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                visTabs = "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags/all",
                                rel="tooltip",
                                data=[("original-title", "All Your Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("globe"), link=c.baseURL+"/your/flags/public",
                                rel="tooltip",
                                data=[("original-title", "Your Public Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li>" + ps.baseAnchor(ps.baseIcon("eye-close"), link=c.baseURL+"/your/flags/private",
                                rel="tooltip",
                                data=[("original-title", "Your Private Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li>" + ps.baseAnchor(ps.baseIcon("search"), link="#search",
                                rel="tooltip",
                                data=[("original-title", "Search Your"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs =  ps.baseColumn(ps.baseUL(visTabs, classes="nav nav-pills"), width=1, classes="pull-right")

                buildMessage = "You have no flags at the moment, but if you want to add one, simply click the button up above to get started!."

                if flags:
                        flagList = fc.flagThumbnails(flags)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow([ps.baseColumn(flagList, width=10), visTabs]) + ps.baseRow(ps.baseColumn(pager, width=10))


@route("/your/flags/private")
class flagIndexPrivate(profileObject):
        def GET(self):
                """
                """
                self.view.tabbar = True
                self.view["title"] = "Your Private Flags"

                new = ps.baseSplitDropdown(btn=ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                        classes="btn-info", link=c.baseURL+"/flags/new"),
                        dropdown=ps.baseMenu(name="flagDropdown",
                                items=[{"name": "%s Note" % ps.baseIcon("list-alt"), "link": c.baseURL+"/flags/new/note"},
                                {"name": "%s Bookmark" % ps.baseIcon("bookmark"), "link": c.baseURL+"/flags/new/bookmark"}]
                                ),
                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                classes="dropdown-toggle btn-info",
                                data=[("toggle", "dropdown"),
                                ("original-title", "Quick select"),
                                ("placement", "bottom")],
                                rel="tooltip"),
                        classes="pull-right")


                start = int(self.members["start"]) if self.members.has_key("start") else 0

                flags = fm.flagList(c.session.userID, True, private=True)

                nextClass = ""
                prevClass = ""

                if start == 0:
                        prevClass = "disabled"
                        prevLink = "#"
                elif start == 10:
                        prevLink = c.baseURL+"/your/flags/private"
                else:
                        prevLink = c.baseURL+"/your/flags/private?start=" + str(start-10)

                if len(flags[start+10:start+20]) <= 0:
                        nextClass = "disabled"
                        nextLink = "#"
                else:
                        nextLink = c.baseURL+"/your/flags/private?start=" + str(start+10)

                flags = flags[start:start+10]

                pager = """<ul class="pager">
        <li class="previous %s">
                <a href="%s">&larr; Previous</a>
        </li>
        <li class="next %s">
                <a href="%s">Next &rarr;</a>
        </li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)


                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("user"), link=c.baseURL+"/you",
                                rel="tooltip",
                                data=[("original-title", "Your Profile"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags",
                                rel="tooltip",
                                data=[("original-title", "Your Flags"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("tags"), link=c.baseURL+"/your/labels",
                                rel="tooltip",
                                data=[("original-title", "Your Labels"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("cogs"), link=c.baseURL+"/your/settings",
                                rel="tooltip",
                                data=[("original-title", "Your Settings"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += new

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Your Flags" % (ps.baseIcon("flag")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                visTabs = "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags/all",
                                rel="tooltip",
                                data=[("original-title", "All Your Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li>" + ps.baseAnchor(ps.baseIcon("globe"), link=c.baseURL+"/your/flags/public",
                                rel="tooltip",
                                data=[("original-title", "Your Public Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("eye-close"), link=c.baseURL+"/your/flags/private",
                                rel="tooltip",
                                data=[("original-title", "Your Private Flags"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs += "<li>" + ps.baseAnchor(ps.baseIcon("search"), link="#search",
                                rel="tooltip",
                                data=[("original-title", "Search Your"),
                                        ("placement", "left"),
                                        ("toggle", "tab")]) +"</li><br />"

                visTabs =  ps.baseColumn(ps.baseUL(visTabs, classes="nav nav-pills"), width=1, classes="pull-right")

                buildMessage = "You have no flags at the moment, but if you want to add one, simply click the button up above to get started!."

                if flags:
                        flagList = fc.flagThumbnails(flags)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow([ps.baseColumn(flagList, width=10), visTabs]) + ps.baseRow(ps.baseColumn(pager, width=10))


@route("/your/labels")
class labelIndex(profileObject):
        def GET(self):
                labelList = lm.labelList(user=c.session.userID)

                new = ps.baseSplitDropdown(btn=ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                        classes="btn-info", link=c.baseURL+"/flags/new"),
                        dropdown=ps.baseMenu(name="flagDropdown",
                                items=[{"name": "%s Note" % ps.baseIcon("list-alt"), "link": c.baseURL+"/flags/new/note"},
                                {"name": "%s Bookmark" % ps.baseIcon("bookmark"), "link": c.baseURL+"/flags/new/bookmark"}]
                                ),
                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                classes="dropdown-toggle btn-info",
                                data=[("toggle", "dropdown"),
                                ("original-title", "Quick select"),
                                ("placement", "bottom")],
                                rel="tooltip"),
                        classes="pull-right")
                self.view["title"] = "Your Labels"

                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("user"), link=c.baseURL+"/you",
                                rel="tooltip",
                                data=[("original-title", "Your Profile"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags",
                                rel="tooltip",
                                data=[("original-title", "Your Flags"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("tags"), link=c.baseURL+"/your/labels",
                                rel="tooltip",
                                data=[("original-title", "Your Labels"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("cogs"), link=c.baseURL+"/your/settings",
                                rel="tooltip",
                                data=[("original-title", "Your Settings"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += new

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Your Labels" % (ps.baseIcon("tags")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                if not labelList:
                        labelList = "Oh no! You don't have any labels currently!"

                self.view.body = pageHead+labelList


@route("/you")
class userIndex(profileObject):
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
                                ("original-title", "Quick select"),
                                ("placement", "bottom")],
                                rel="tooltip"),
                        classes="pull-right")
                tabs = "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("user"), link=c.baseURL+"/you",
                                rel="tooltip",
                                data=[("original-title", "Your Profile"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags",
                                rel="tooltip",
                                data=[("original-title", "Your Flags"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("tags"), link=c.baseURL+"/your/labels",
                                rel="tooltip",
                                data=[("original-title", "Your Labels"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("cogs"), link=c.baseURL+"/your/settings",
                                rel="tooltip",
                                data=[("original-title", "Your Settings"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += new

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s You" % (ps.baseIcon("user")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                email = " %s"%c.session.user["email"] if c.session.user["email"] else " You don't have an email registered!"

                if not c.session.user["emailVisibility"]:
                        emailVis = ps.baseLabel("%s Private" % ps.baseIcon("eye-close"))
                else:
                        emailVis = ps.baseLabel("%s Public" % ps.baseIcon("globe"))


                if not c.session.user["visibility"]:
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
                                        width=10
                                        )
                                ])

                about = c.session.user["about"] or "You don't have anything about you yet!"

                content += ps.baseRow(ps.baseColumn(about))


                self.view.body = pageHead + content

@route("/your/settings")
class userEdit(profileObject):
        def GET(self):
                """
                """
                self.view.sidebar = ""
                user = profilem.profile(c.session.userID, md=False)
                self.view["title"] = "Editing your settings"

                new = ps.baseSplitDropdown(btn=ps.baseAButton("%s New Flag" % ps.baseIcon("flag"),
                        classes="btn-info", link=c.baseURL+"/flags/new"),
                        dropdown=ps.baseMenu(name="flagDropdown",
                                items=[{"name": "%s Note" % ps.baseIcon("list-alt"), "link": c.baseURL+"/flags/new/note"},
                                {"name": "%s Bookmark" % ps.baseIcon("bookmark"), "link": c.baseURL+"/flags/new/bookmark"}]
                                ),
                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                classes="dropdown-toggle btn-info",
                                data=[("toggle", "dropdown"),
                                ("original-title", "Quick select"),
                                ("placement", "bottom")],
                                rel="tooltip"),
                        classes="pull-right")
                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("user"), link=c.baseURL+"/you",
                                rel="tooltip",
                                data=[("original-title", "Your Profile"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link=c.baseURL+"/your/flags",
                                rel="tooltip",
                                data=[("original-title", "Your Flags"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("tags"), link=c.baseURL+"/your/labels",
                                rel="tooltip",
                                data=[("original-title", "Your Labels"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("cogs"), link=c.baseURL+"/your/settings",
                                rel="tooltip",
                                data=[("original-title", "Your Settings"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += new

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Your Settings" % (ps.baseIcon("cogs")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/your/settings"),
                        method="POST",
                        actions=[ps.baseSubmit("%s Update!"%ps.baseIcon("save"), classes="btn-info")],
                        fields=[
                                ps.baseHeading("Edit your profile %s" % ps.baseSmall("About you and visibility to the public..."), size=3),
                                {"label": "Profile Visibility", "content": ps.baseCheckbox(name="visibility", checked=user["visibility"], label="If you want others to be able to find you, check this box.")},
                                {"content": ps.baseTextarea(user["about"], name="about", classes="span10"), "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"))},
                                ps.baseHeading("Set or update an email? %s" % ps.baseSmall("Just for us to contact you with..."), size=3),

                                {"content": ps.baseInput(type="email", name="email", placeholder="email@email.com", classes="span10", value=user["email"]), "help": ps.baseSmall("You don't have to register an email, and can remove it at anytime. We do not give away your email, or sell it for profit or otherwise.")},
                                {"label": "Email Visibility", "content": ps.baseCheckbox(name="emailVisibility", checked=user["emailVisibility"], label="If you have a registered email, and want others to be able to find it, check this box.")},
                                ps.baseHeading("Change your password? %s" % ps.baseSmall("You don't have to..."), size=3),
                                {"content": ps.baseInput(type="password", name="oldpassword", placeholder="Old password", classes="span10")},
                                "<br><br>",
                                {"content": ps.baseInput(type="password", name="newpassword", placeholder="New password", classes="span10")},
                                "<br><br>",
                                {"content": ps.baseInput(type="password", name="newtwopassword", placeholder="Repeat New password", classes="span10")},
                                ]
                       , classes="span10")

                self.view["body"] = pageHead + editForm

        def POST(self):
                """
                """
                if not self.members.has_key("visibility"): self.members["visibility"] = False
                if not self.members.has_key("emailVisibility"): self.members["emailVisibility"] = False

                try:
                        user = profilem.profile(c.session.userID)
                        user["visibility"] = self.members["visibility"]
                        user["emailVisibility"] = self.members["emailVisibility"]
                        user["about"] = self.members["about"]
                        user["email"] = self.members["email"]

                        user.commit()

                        if self.members["oldpassword"]:
                                if user["password"] == bcrypt.hashpw(self.members["oldpassword"], user["password"]):
                                        if self.members["newpassword"] == self.members["newtwopassword"]:
                                                password = self.members["newpassword"]
                                        else:
                                                raise Exception("New passwords need to match!")
                                else:
                                        raise Exception("Old password doesn't match your current password!")

                        user.commit()

                        self.head = ("303 SEE OTHER", [("location", "/you")])
                        c.session.pushAlert(("You've updated your settings!"), title="Congratulations!", icon="ok", type="success")

                except Exception as exc:
                        self.head = ("303 SEE OTHER", [("location", "/your/settings")])
                        c.session.pushAlert("Something went wrong while updating your profile.<br>%s Heres the edit form again. Sorry!" % exc, icon="fire", title="OH SNAP!", type="error")
