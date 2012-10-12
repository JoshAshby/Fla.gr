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

import bcrypt


class basePost(blm.baseBlockModel):
        fields = ["otherEnd",
                "otherEndID",
                "sender",
                "senderID",
                "message",
                "sentTime",
                "read",
                "replyTo",
                "subject",
                ]

        objectID = "message"
        dbName = "redisUserServer"

        def new(self):
                self.sender = c.session.user["username"]
                self.sentTime = dt.utcnow().strftime("%b-%d-%Y %I:%M %p")
