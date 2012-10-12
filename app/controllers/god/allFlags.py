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
from seshat.route import route
import views.pyStrap.pyStrap as ps

import flagr.models.flagModel as fm


@route("/god/flags")
class flagsIndex_god(basePage):
        __menu__ = "Deity Flags"
        def GET(self):
                pass
