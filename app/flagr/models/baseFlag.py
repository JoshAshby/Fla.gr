#!/usr/bin/env python2
"""
Fla.gr - Personal Memory
Database model for flags. This uses blocks so each
        field could be a different type and entry in redis,
        however the baseBlockModel takes care of all that logic
        for us. In theory it doesn't even have to be
        redis either so long as the blocks all use
        the same interface.


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


class baseFlag(blm.baseBlockModel):
        fields = ["title",
                "description",
                "author",
                "time",
                ("visibility", "string", helpers.boolean),
                "userID",
                ("labels", "set", unicode),
                "flagType"]

        objectID = "flag"
        dbName = "redisFlagServer"
        icon="list"

        def new(self):
                self.author = c.session.user.username
                self.userID = c.session.userID

                self.time = dt.utcnow().strftime("%b-%d-%Y %I:%M %p")
                self.flagType = self.flag
