#!/usr/bin/env python
"""
fla.gr controller for viewing a specific users profile

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.user.userProfileTmpl import userProfileTmpl

import models.user.userModel as um

@route("/user/(.*)")
class adminUsers(baseHTMLObject):
    __name__ = "user profile"
    def GET(self):
        """
        """
        userID = self.env["members"][0]

        user = um.findUserByID(userID) or um.findUserByUsername(userID)
        view = userProfileTmpl(searchList=[self.tmplSearchList])

        view.userProfile = user

        return view
