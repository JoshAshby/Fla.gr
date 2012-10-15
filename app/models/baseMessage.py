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


class baseMessage(blm.baseBlockModel):
        fields = ["user",
                "sender",
                "message",
                "sentTime",
                ("read", "string", helpers.boolean),
                "replyTo",
                "subject",
                ("archive", "string", helpers.boolean)
                ]

        objectID = "message"
        dbName = "redisUserServer"

        def new(self):
                self.sender = c.session.userID
                self.sentTime = dt.utcnow().strftime("%b-%d-%Y %I:%M %p")
