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

from flagr.objects.flagrObject import flagrObject as flagrPage
from seshat.route import route

import views.pyStrap.pyStrap as ps


@route("/profiles")
class userIndex(flagrPage):
        def GET(self):

        def POST(self):



@route("/profiles/edit")
class userEdit(flagrPage):
        def GET(self):

        def POST(self):



@route("/profiles/view/(.*)")
class userView(flagrPage):
        def GET(self):

        def POST(self):


