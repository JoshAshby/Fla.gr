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
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.user.userLabelTmpl import userLabelTmpl

import models.flag.flagModel as fm
import models.user.userModel as um
import utils.labelUtils as lu

@route("/user/(.*)/labels")
class userLabels(baseHTMLObject):
    _title = "labels"
    def GET(self):
        """
        """
        user = self.env["members"][0]
        view = userLabelTmpl(searchList=[self.tmplSearchList])
        user = um.userORM.find(user)

        flags = fm.listFlagsByUserID(user.id)
        if flags:
            for flag in flags:
                if not flag.visibility:
                    flags.pop(flags.index(flag))

        labels = lu.listLabels(flags, False)

        view.labels = labels
        view.flagAuthor = user

        return view
