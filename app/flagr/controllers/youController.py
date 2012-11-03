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


@route("/your/flags(.*)")
class flagIndexPublic(profileObject):
    def GET(self):
        """
        """
        self.view.tabbar = True
        typer = self.members[0].strip("/")

        if typer == "private":
            title = "Private"
            flags = fm.flagList(c.session.userID, True, private=True)
            visTabsDict = [{"link": c.baseURL+"/your/flags",
                    "icon": "flag",
                    "title": "All of your flags"},
                {"link": c.baseURL+"/your/flags/public",
                    "icon": "globe",
                    "title": "Your Public"},
                {"active": True,
                    "link": c.baseURL+"/your/flags/private",
                    "icon": "eye-close",
                    "title": "Your private flags"}]
        elif typer == "public":
            title = "Public "
            flags = fm.flagList(c.session.userID, True, public=True)
            visTabsDict = [{"link": c.baseURL+"/your/flags",
                    "icon": "flag",
                    "title": "All of your flags"},
                {"active": True,
                    "link": c.baseURL+"/your/flags/public",
                    "icon": "globe",
                    "title": "Your Public"},
                {"link": c.baseURL+"/your/flags/private",
                    "icon": "eye-close",
                    "title": "Your private flags"}]
        else:
            title = ""
            flags = fm.flagList(c.session.userID, True)
            visTabsDict = [{"active": True,
                    "link": c.baseURL+"/your/flags",
                    "icon": "flag",
                    "title": "All of your flags"},
                {"link": c.baseURL+"/your/flags/public",
                    "icon": "globe",
                    "title": "Your Public"},
                {"link": c.baseURL+"/your/flags/private",
                    "icon": "eye-close",
                    "title": "Your private flags"}]

        self.view["title"] = "Your %sFlags" % title

        flags, pager = fc.listPager(flags,
                "/your/flags/%s" % typer,
                self.members)

        tabs = fc.tabs([
            {"link": c.baseURL+"/you",
                "title": "Your Profile",
                "icon": "user"},
            {"active": True,
                "link": c.baseURL+"/your/flags",
                "title": "Your Flags",
                "icon": "flag"},
            {"link": c.baseURL+"/your/labels",
                "title": "Your Labels",
                "icon": "tags"},
            {"link": c.baseURL+"/your/settings",
                "title": "Your Settings",
                "icon": "cogs"},
            ],
            fc.newFlagButton)

        pageHead = ps.baseRow([
            ps.baseColumn(
                ps.baseHeading("%s Your %sFlags" %
                        (ps.baseIcon("flag"),
                        title),
                    size=2),
                width=5),
            ps.baseColumn(tabs,
                width=5)
            ])

        visTabs = fc.tabs(visTabsDict,
            classes="pills")

        visTabs =  ps.baseColumn(visTabs,
            width=1,
            classes="pull-right")

        buildMessage = "You have no flags at the moment, but if you want to add one, simply click the button up above to get started!."

        if flags:
            flagList = fc.flagThumbnails(flags)
        else:
            flagList = buildMessage

        self.view.body = pageHead
        self.view.body += ps.baseRow([
            ps.baseColumn(flagList,
                width=10),
            visTabs])
        self.view.body += ps.baseRow(
            ps.baseColumn(pager,
                width=10)
            )


@route("/your/labels")
class labelIndex(profileObject):
    def GET(self):
        labelList = lm.labelList(user=c.session.userID)

        self.view["title"] = "Your Labels"

        tabs = fc.tabs([
            {"link": c.baseURL+"/you",
                "title": "Your Profile",
                "icon": "user"},
            {"link": c.baseURL+"/your/flags",
                "title": "Your Flags",
                "icon": "flag"},
            {"active": True,
                "link": c.baseURL+"/your/labels",
                "title": "Your Labels",
                "icon": "tags"},
            {"link": c.baseURL+"/your/settings",
                "title": "Your Settings",
                "icon": "cogs"},
            ],
            fc.newFlagButton)

        pageHead = ps.baseRow([
            ps.baseColumn(
                ps.baseHeading("%s Your Labels" % (ps.baseIcon("tags")),
                    size=2),
                width=5),
            ps.baseColumn(tabs,
                width=5)
            ])

        if not labelList:
            labelList = "Oh no! You don't have any labels currently!"

        self.view.body = pageHead
        self.view.body += labelList


@route("/you")
class userIndex(profileObject):
    def GET(self):
        self.view["title"] = "You!"

        tabs = fc.tabs([
            {"active": True,
                "link": c.baseURL+"/you",
                "title": "Your Profile",
                "icon": "user"},
            {"link": c.baseURL+"/your/flags",
                "title": "Your Flags",
                "icon": "flag"},
            {"link": c.baseURL+"/your/labels",
                "title": "Your Labels",
                "icon": "tags"},
            {"link": c.baseURL+"/your/settings",
                "title": "Your Settings",
                "icon": "cogs"},
            ],
            fc.newFlagButton)

        pageHead = ps.baseRow([
            ps.baseColumn(
                ps.baseHeading("%s You" % (ps.baseIcon("user")),
                    size=2),
                width=5),
            ps.baseColumn(tabs,
                width=5)
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
                    ps.baseColumn(
                        ps.baseBold("Profile: ", classes="muted")
                    ) +
                    ps.baseColumn(vis) +
                    ps.baseColumn(
                        ps.baseBold("Email: ", classes="muted")
                    ) +
                    ps.baseColumn(emailVis + email)
                ), width=10
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

        tabs = fc.tabs([
            {"link": c.baseURL+"/you",
                "title": "Your Profile",
                "icon": "user"},
            {"link": c.baseURL+"/your/flags",
                "title": "Your Flags",
                "icon": "flag"},
            {"link": c.baseURL+"/your/labels",
                "title": "Your Labels",
                "icon": "tags"},
            {"active": True,
                "link": c.baseURL+"/your/settings",
                "title": "Your Settings",
                "icon": "cogs"},
            ],
            fc.newFlagButton)

        pageHead = ps.baseRow([
            ps.baseColumn(
                ps.baseHeading("%s Your Settings" % (ps.baseIcon("cogs")),
                    size=2),
                width=5),
            ps.baseColumn(tabs,
                width=5)
            ])

        editForm = ps.baseHorizontalForm(
                action=(c.baseURL+"/your/settings"),
            method="POST",
            actions=[ps.baseSubmit("%s Update!"%ps.baseIcon("save"),
                classes="btn-info")],
            fields=[
                ps.baseHeading("Edit your profile %s" % ps.baseSmall("About you and visibility to the public..."),
                    size=3),
                {"label": "Profile Visibility",
                    "content": ps.baseCheckbox(name="visibility",
                        checked=user["visibility"],
                        label="If you want others to be able to find you, check this box.")},
                {"content": ps.baseTextarea(user["about"],
                    name="about",
                    classes="span10"),
                    "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"))},
                ps.baseHeading("Set or update an email? %s" % ps.baseSmall("Just for us to contact you with..."),
                    size=3),

                {"content": ps.baseInput(type="email",
                    name="email",
                    placeholder="email@email.com",
                    classes="span10",
                    value=user["email"]),
                    "help": ps.baseSmall("You don't have to register an email, and can remove it at anytime. We do not give away your email, or sell it for profit or otherwise.")},
                {"label": "Email Visibility",
                    "content": ps.baseCheckbox(name="emailVisibility",
                        checked=user["emailVisibility"],
                        label="If you have a registered email, and want others to be able to find it, check this box.")},
                ps.baseHeading("Change your password? %s" % ps.baseSmall("You don't have to..."),
                    size=3),
                {"content": ps.baseInput(type="password",
                    name="oldpassword",
                    placeholder="Old password",
                    classes="span10")},
                "<br><br>",
                {"content": ps.baseInput(type="password",
                    name="newpassword",
                    placeholder="New password",
                    classes="span10")},
                "<br><br>",
                {"content": ps.baseInput(type="password",
                    name="newtwopassword",
                    placeholder="Repeat New password",
                    classes="span10")},
                ],
            classes="span10")

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
                if user["password"] == bcrypt.hashpw(self.members["oldpassword"],
                    user["password"]):
                    if self.members["newpassword"] == self.members["newtwopassword"]:
                        user["password"] = self.members["newpassword"]
                    else:
                        raise Exception("New passwords need to match!")
                else:
                    raise Exception("Old password doesn't match your current password!")

            user.commit()

            self.head = ("303 SEE OTHER", [("location", "/you")])
            c.session.pushAlert(("You've updated your settings!"),
                title="Congratulations!",
                icon="ok",
                type="success")

        except Exception as exc:
            self.head = ("303 SEE OTHER", [("location", "/your/settings")])
            c.session.pushAlert("Something went wrong while updating your profile.<br>%s Heres the edit form again. Sorry!" % exc,
                icon="fire",
                title="OH SNAP!",
                type="error")
