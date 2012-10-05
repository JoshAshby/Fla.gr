#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
Main index file.

For more information, see: https://github.com/JoshAshby/

**WARNING**
Make sure you look through and change things in config.py
before running this file, to be sure it runs the way you want it to

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import sys, os

try:
        import config as c
except:
        abspath = os.path.dirname(__file__)
        sys.path.append(abspath)
        os.chdir(abspath)
        import config as c

import seshat.framework as fw
from objects.userObject import userObject as basePage
from seshat.route import route

import models.basic.postModel as pm
import views.pyStrap.pyStrap as ps


@route("/")
class index(basePage):
        __menu__ = "Home"
        """
        Returns base index page.
        """
        def GET(self):
                """

                """
                hero = ps.baseHeading(ps.baseIcon("flag")+" Welcome to fla.gr!", size=1)
                hero += ps.baseParagraph("Fla.gr is a place to store web memories. Whether they are just notes, a webpage, or a neat book or some other oddity of the web, you can find (or better yet make) a flag for it!")

                hero = ps.baseHero(hero)
                posts = pm.postList()

                postListRows = ""
                if posts:
                        for post in posts:
                                if c.session.loggedIn and c.session.user.level in ["GOD", "admin"]:
                                        edit = ps.baseButtonGroup([ps.baseAButton("Edit this post", link=c.baseURL + "/admin/posts/edit/%s"%post.id, classes="btn-info"),
                                                ps.baseAButton("Delete this post", link=c.baseURL+"/admin/posts/delete/%s"%post.id, classes="btn-danger")])
                                else:
                                        edit = ""

                                title = post.title + ps.baseSmall(" Posted by: "+post.author)

                                postListRows += """
                                %(title)s
                                %(post)s
                                Posted/Last Updated at: %(time)s
                                %(edit)s
                                <hr>
                                """ % {"title": ps.baseHeading(title, size=2),
                                        "post": post.post,
                                        "time": ps.baseSmall(post.time),
                                        "edit": edit}
                else:
                        postListRows = "Well it would look like we don't have any news to bring you just this moment, however stay tuned!"


                self.view.body = hero + postListRows


from controllers.authController import *
from controllers.adminController import *
from controllers.godController import *


#Fla.gr specific code. Makes for easy modulation of the system...
from flagr.controllers.flagController import *
#from flagr.controllers.profileController import *
#from flagr.controllers.labelController import *

#from test import *


if __name__ == '__main__':
        """
        Because we're not doing anything else yet, such as starting a websockets
        server or whatever, we're going to just go into forever serve mode.
        """
        fw.forever()
