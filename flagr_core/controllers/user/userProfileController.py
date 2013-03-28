#!/usr/bin/env python
"""
fla.gr controller for viewing a specific users profile
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.user.userProfileTmpl import userProfileTmpl

import models.user.userModel as um


@route("/user/(.*)")
class userProfile(baseHTMLObject):
    __name__ = "profile"
    def GET(self):
        """
        """
        userID = self.env["members"][0]

        user = um.userORM.find(userID)
        view = userProfileTmpl(searchList=[self.tmplSearchList])

        view.userProfile = user

        return view
