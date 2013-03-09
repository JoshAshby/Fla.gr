#!/usr/bin/env python
"""
fla.gr controller for viewing the logged in users flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youFlagsTmpl import youFlagsTmpl

import models.flag.flagModel as fm


@route("/your/flags")
class youFlags(baseHTMLObject):
    __name__ = "flags"
    __login__ = True
    def GET(self):
        """
        """
        view = youFlagsTmpl(searchList=[self.tmplSearchList])

        flags = fm.listFlagsByUserID(self.session.id)
        if flags:
            flags = fm.formatFlags(flags, True)

        view.flags = flags

        return view
