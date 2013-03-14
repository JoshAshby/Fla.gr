#!/usr/bin/env python
"""
fla.gr controller for editing flags

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.flags.flagViewTmpl import flagViewTmpl

import models.flag.flagModel as fm
import models.user.userModel as um
import config.dbBase as db


@route("/flags/(.*)")
class flagView(baseHTMLObject):
    __name__ = "view flag"
    def GET(self):
        """
        """
        flagid = self.env["members"][0]
        flag = fm.flagORM.load(db.couchServer, flagid)
        print flag
        if not flag.visibility and flag.userID != self.session.id:
            self.session.pushAlert("This is a private flag! Sorry but we can't let you see it.", "Hold it.", "error")
            self.head = ("303 SEE OTHER", [("location", "/flags")])
            return

        view = flagViewTmpl(searchList=[self.tmplSearchList])

        flag = fm.formatFlag(flag)

        view.flag = flag

        user = um.userORM.load(db.couchServer, flag.userID)
        view.flagAuthor = user

        return view

