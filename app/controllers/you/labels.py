#!/usr/bin/env python
"""
fla.gr controller for viewing the logged in users labels

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute, route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youLabelsTmpl import youLabelsTmpl

import models.couch.flag.collections.userPublicFlagsCollection as pubfc
import models.couch.flag.collections.userPrivateFlagsCollection as privfc
import utils.labelUtils as lu


@route("/your/labels")
@autoRoute()
class youLabels(baseHTMLObject):
    _title = "labels"
    __login__ = True
    def GET(self):
        """
        """
        view = youLabelsTmpl(searchList=[self.tmplSearchList])

        privateFlags = privfc.userPrivateFlagsCollection(self.session.id)
        privateFlags.fetch()
        publicFlags = pubfc.userPublicFlagsCollection(self.session.id)
        publicFlags.fetch()

        privateFlags.tub.extend(publicFlags.tub)
        flags = privateFlags.tub

        labels = lu.listLabels(flags)

        view.labels = labels

        return view
