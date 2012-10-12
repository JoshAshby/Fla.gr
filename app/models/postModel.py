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
import models.posts.normalPost as np
import models.blocks.helpers as helpers
import markdown

def post(id=None, md=False):
        if id:
                key = id.strip("post:")
                returnPost = np.normalPost(key)
                if md:
                        returnPost["post"] = markdown.markdown(returnPost["post"])
        if not id:
                returnPost = np.normalPost()

        return returnPost

def postList(md=False):
        keys = c.redisPostServer.keys("post:*:id")
        postList = []
        def addPost(key):
                returnPost = post(key, md)

                postList.append(returnPost)

        for key in keys:
                key = key.strip(":id")
                addPost(key)

        return postList
