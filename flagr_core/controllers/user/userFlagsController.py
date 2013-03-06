#!/usr/bin/env python
"""
fla.gr controller for viewing a given users public flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.user.userFlagsTmpl import userFlagsTmpl

import models.flag.flagModel as fm


@route("/user/(.*)/flags")
class userFlags(baseHTMLObject):
    __name__ = "user flags"
    def GET(self):
        """
        """
        view = userFlagsTmpl(searchList=[self.tmplSearchList])

        flags = fm.listFlagsByUserID(self.session.id)
        if flags:
            flags = fm.formatFlags(flags)

        for flag in flags:
            if not flag.visibility:
                flags.pop(flags.index(flag))

        view.flags = flags

        return view
