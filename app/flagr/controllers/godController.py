#!/usr/bin/env python
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

from seshat.route import route

from flagr.objects.userObject import userObject
from flagr.objects.godObject import godObject
import flagr.views.pyStrap.pyStrap as ps

from flagr.controllers.god.allFlags import *

import models.profileModel as profilem


@route("/god")
class godIndex_god(godObject):
    __menu__ = "Deity Panel"
    def GET(self):
        """
        """
        hero = ps.baseHeading(ps.baseIcon("eye-open") + " Welcome, Deity", size=1)
        hero += ps.baseParagraph("This is the deity panel. From here, you will be able to control and view information concerning several aspects of the website which no one else has access to.")

        page = ps.baseTextThumbnail(
            label=ps.baseHeading(
                ps.baseIcon("flag") + " All the Flags"),
            caption=ps.baseParagraph("""
Edit, delete and manage every flag in fla.gr....
<br />
<br />
%s
""" % ps.baseAButton("%s Flags"%ps.baseIcon("flag"),
                link=c.baseURL+"/god/flags",
                classes="btn-info")
                ),
            classes="span3")
        page += ps.baseTextThumbnail(
            label="",
            caption="",
            classes="span4")
        page += ps.baseTextThumbnail(
            label="",
            caption="",
            classes="span3")

        self.view["body"] = ps.baseHero(hero)
        self.view.body += ps.baseUL(page,
                classes="thumbnails")
        self.view.sidebar = ""


@route("/god/setup")
class setup(userObject):
    def GET(self):
        """
        """
        user = profilem.profile()
        user["username"] = "JoshAshby"
        user["level"] = "GOD"
        user["adminNotes"] = ""
        user["password"] = "josh"
        user["about"] = """#Hi there!

My names transientBug, but you can also call me Josh. I'm the programmer and developer of fla.gr!
        """
        user["visibility"] = True
        user["emailVisibility"] = True
        user["email"] = "joshuaashby@joshashby.com"

        user.commit()

        self.view["title"] = "Initial Setup"
        self.view["body"] = "User JoshAshby with password josh has been created."
