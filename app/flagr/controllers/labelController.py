#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

label controller. Everything under the /labels
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


@route("/labels")
class labelIndex(flagrPage):
        def GET(self):
                pass


@route("/labels/view/(.*)")
class labelView(flagrPage):
        def GET(self):
                labels = self.members[0]
                self.view.body = labels

