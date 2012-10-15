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
import models.profileModel as profilem

from controllers.god.allFlags import *
from controllers.god.allLabels import *

@route("/god")
class godIndex_god(basePage):
        __menu__ = "Deity Panel"
        def GET(self):
                """
                """
                hero = ps.baseHeading(ps.baseIcon("eye-open") + " Welcome, Deity", size=1)
                hero += ps.baseParagraph("This is the deity panel. From here, you will be able to control and view information concerning several aspects of the website which no one else has access to.")

                pageHead = ps.baseRow(hero)

                page = ""

                self.view["body"] = ps.baseHero(hero) + ps.baseUL(page, classes="thumbnails")
                self.view.sidebar = ""
                self.view.scripts = ps.baseScript("""
                $('.btn-group').tooltip({
                      selector: "a[rel=tooltip]"
                })
""")


@route("/god/setup")
class setup(setupPage):
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
