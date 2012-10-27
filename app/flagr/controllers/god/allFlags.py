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


@route("/god/flags")
class flagsIndex_god(godObject):
        __menu__ = "Deity Flags"
        def GET(self):
                pass

@route("/god/flag/(.*)/edit")
class flagEdit_god(godObject):
        def GET(self):
                pass

        def POST(self):
                pass

@route("/god/flag/(.*)/delete")
class flagDelete_god(godObject):
        def GET(self):
                pass

        def POST(self):
                pass

@route("/god/flag/(.*)/copy")
class flagCopy_god(godObject):
        def GET(self):
                pass

        def POST(self):
                pass

@route("/god/flag/(.*)")
class flagView_god(godObject):
        def GET(self):
                pass

        def POST(self):
                pass
