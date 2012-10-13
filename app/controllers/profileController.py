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

from objects.profileObject import profileObject as profilePage
from objects.profileObject import publicProfileObject as publivProfilePage
from seshat.route import route

import views.pyStrap.pyStrap as ps


@route("/you")
@route("/profile")
class userIndex(profilePage):
        def GET(self):
                
                pass

        def POST(self):
                pass


@route("/you/edit")
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
