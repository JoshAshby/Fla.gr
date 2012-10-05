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

from objects.godObject import godObject as basePage
from objects.userObject import userObject as setupPage
from seshat.route import route
import views.pyStrap.pyStrap as ps
import models.basic.authModel as am


@route("/god")
class godIndex_god(basePage):
        __menu__ = "Deity Panel"
        def GET(self):
                """
                """
                hero = ps.baseHeading(ps.baseIcon("eye-open") + " Welcome, Deity", size=1)
                hero += ps.baseParagraph("This is the deity panel. From here, you will be able to control and view information concerning several aspects of the website which no one else has access to.")

                content = ps.baseParagraph("It would seem your minions are well behaved today. As a result, you might want to take a look at the sidebar for things to do, me lord.")

                self.view.body = ps.baseHero(hero) + content


@route("/god/setup")
class setup(setupPage):
        def GET(self):
                """
                """
                user = am.baseUser()
                user["username"] = "Josh"
                user["level"] = "GOD"
                user["notes"] = ""
                user.password = "josh"

                user.commit()

                self.view["title"] = "Initial Setup"
                self.view["body"] = "User Josh with password josh has been created."
