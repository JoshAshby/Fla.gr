#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
controller for authentication stuff.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from seshat.route import route

import flagr.views.pyStrap.pyStrap as ps
from flagr.objects.adminObject import adminObject
from flagr.controllers.admin.users import *
from flagr.controllers.admin.indexPosts import *
from flagr.controllers.admin.indexNewsCarousel import *


@route("/admin")
class adminIndex_admin(adminObject):
    __menu__ = "Admin Panel"
    def GET(self):
        """
        """
        hero = ps.baseHeading(ps.baseIcon("dashboard") + " Howdy, Admin!",
            size=1)
        hero += ps.baseParagraph("This is the admin panel. Here you can manage aspects of the site such as users, front page posts and sometime later, even more!")

        page = ps.baseTextThumbnail(
            label=ps.baseHeading(ps.baseIcon("rss") + " Blog posts"),
            caption=ps.baseParagraph("""
Edit, delete and create front page blog posts.
<br />
<br />
%s""" % ps.baseAButton("%s Posts"%ps.baseIcon("rss"),
                link=c.baseURL+"/admin/posts",
                classes="btn-info")),
            classes="span3")

        page += ps.baseTextThumbnail(
            label=ps.baseHeading(
                ps.baseIcon("play") + " Carousel"),
            caption=ps.baseParagraph("""
Edit, delete and create front page carousel items.
<br />
<br />
%s""" % ps.baseAButton("%s Carousel"%ps.baseIcon("play"),
                link=c.baseURL+"/admin/carousels",
                classes="btn-info")),
            classes="span4")

        page += ps.baseTextThumbnail(
            label=ps.baseHeading(ps.baseIcon("group") + " Users"),
            caption=ps.baseParagraph("""
Edit, delete and create system users.
<br />
<br />
%s""" % ps.baseAButton("%s Users"%ps.baseIcon("play"),
                link=c.baseURL+"/admin/users",
                classes="btn-info")),
            classes="span3")

        self.view["body"] = ps.baseHero(hero)
        self.view.body += ps.baseUL(page,
                classes="thumbnails")
        self.view.sidebar = ""
