#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
Database model for authentication and users

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from datetime import datetime as dt
import models.basic.baseModel as bm

import markdown
import string
import random


def postList(md=True):
        posts = []
        for key in c.redisPostServer.keys("post:*"):
                post = basePost(key[5:])
                if md:
                        try:
                                post["post"] = str(markdown.markdown(post["post"]))

                        except:
                                pass
                posts.append(post)

        return posts


class basePost(bm.baseRedisModel):
        __dbname__ = "redisPostServer"
        __dbid__ = "post:"
        parts = ["author", "title", "post", "time", "id"]

        def new(self):
                self.time = dt.utcnow().strftime("%b-%d-%Y %I:%M %p")
