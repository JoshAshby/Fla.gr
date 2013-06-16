#!/usr/bin/env python
"""
fla.gr controller for viewing a given users public labels

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from utils.baseHTMLObject import baseHTMLObject

from views.user.userLabelTmpl import userLabelTmpl

import models.couch.flag.flagModel as fm
import models.couch.flag.collections.userPublicFlagsCollection as pubfc
import models.couch.user.userModel as um
import utils.labelUtils as lu


@autoRoute()
class userLabels(baseHTMLObject):
    _title = "labels"
    def GET(self):
        """
        """
        user = self.env["members"][0]
        view = userLabelTmpl(searchList=[self.tmplSearchList])
        user = um.userORM.find(user)

        flags = pubfc.userPublicFlagsCollection(user.id)
        flags.paginate(page, 25)
        flags.fetch()

        labels = lu.listLabels(flags)

        view.labels = labels
        view.flagAuthor = user

        return view
