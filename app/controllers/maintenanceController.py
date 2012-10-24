#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
Main index file.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from objects.userObject import userObject as basePage
from seshat.route import route

import views.pyStrap.pyStrap as ps


@route("/(.*)")
class maintenance(basePage):
        """
        Returns base maintenance page
        """
        def GET(self):
                """

                """
                self.view.title = "Down for Maintenance"
                content = ps.baseHeading("%s Maintenance!" % ps.baseIcon("fire"), size=1)
                content += ps.baseParagraph("We're crrently down for maintenance! Give us a few minutes and hopefully we'll be back up!")
                hero = ps.baseHero(content)

                self.view.body = hero
