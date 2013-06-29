#!/usr/bin/env python
"""
fla.gr controller to view an individual user

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseHTMLObject import baseHTMLObject
from seshat.objectMods import *

from models.couch.user.userModel import userORM


@autoRoute()
@admin()
class view(baseHTMLObject):
    _title = "flagpole user"
    _defaultTmpl = "flagpole/users/singleUser"
    def GET(self):
        """
        """
        userid = self.request.id
        user = userORM.find(userid)

        print userid

        self.view.data = {"user": user}
        return self.view
