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

from flagr.objects.godObject import godObject
from seshat.route import route
import flagr.views.pyStrap.pyStrap as ps

import flagr.models.flagModel as fm


@route("/god/labels")
class labelsIndex_god(godObject):
        __menu__ = "Deity Labels"
        def GET(self):
                pass
