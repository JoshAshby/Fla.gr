#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent

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

import bcrypt


class baseProfile(blm.baseBlockModel):
        fields = ["username",
                "password",
                "adminNotes",
                "creationTime",
                "level",
                ("disable", "string", helpers.boolean),
                #User editable under this, admin only above.
                ("visibility", "string", helpers.boolean),
                "about",
                "email",
                ("emailVisibility", "string", helpers.boolean),
                ]

        objectID = "profile"
        dbName = "redisUserServer"

        def new(self):
                self.creationTime = dt.utcnow().strftime("%b-%d-%Y %I:%M %p")

        def __setitem__(self, item, value):
                if item == "password" and value and value[:7] != "$2a$12$":
                        value = bcrypt.hashpw(value, bcrypt.gensalt())

                item = object.__getattribute__(self, item)
                item.current = value
                return value
