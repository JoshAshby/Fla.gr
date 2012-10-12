#!/usr/bin/env python2
"""


For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c
import models.blocks.baseBlockModel as blm
import models.blocks.helpers as helpers
from datetime import datetime as dt


class basePost(blm.baseBlockModel):
        fields = ["title",
                "post",
                "author",
                "time",
                ("visibility", "string", helpers.boolean),
                "postType",
                "postArea",
                "userID"]

        objectID = "post"
        dbName = "redisPostServer"

        def new(self):
                self.author = c.session.user.username
                self.userID = c.session.userID

                self.time = dt.utcnow().strftime("%b-%d-%Y %I:%M %p")
                self.postType = self.type
                self.postArea = self.area
