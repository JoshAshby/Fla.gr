#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
Main index file.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from objects.userObject import userObject as basePage
from seshat.route import route

import models.postModel as pm
import models.carouselModel as cm
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
                carousel = cm.carouselList(True)

                hero = ""

                if carousel:
                        carouselList = [ ps.baseColumn(item["content"], offset=1, width=6) for item in carousel if item["visibility"] ]

                        if carouselList: hero = ps.baseHero(ps.baseCarousel(items=carouselList, id="frontCarousel"))

                posts = pm.postList(True)

                content = ""
                if posts:
                        for post in posts:
                                if post["visibility"]:
                                        if c.session.loggedIn and c.session.user["level"] in ["GOD", "admin"]:
                                                edit = ps.baseSplitDropdown(btn=ps.baseAButton(ps.baseIcon("zoom-in"),
                                                                classes="",
                                                                link=c.baseURL+"/post/"+post.id,
                                                                data=[("original-title", "Expand Post")],
                                                                rel="tooltip"),
                                                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                                                classes="dropdown-toggle btn-info",
                                                                data=[("toggle", "dropdown"),
                                                                        ("original-title", "More actions")],
                                                                rel="tooltip"),
                                                        dropdown=ps.baseMenu(name="postDropdown",
                                                                items=[{"name": "%s View as admin" % ps.baseIcon("cogs"), "link": c.baseURL+"/admin/post/%s/view"%post.id},
                                                                        {"name": "%s Edit" % ps.baseIcon("edit"), "link": c.baseURL+"/admin/post/%s/edit"%post.id},
                                                                        {"name": ps.baseBold("%s Delete"%ps.baseIcon("trash"), classes="text-error"), "link": c.baseURL+"/admin/post/%s/delete"%post.id}]
                                                                ))
                                        else:
                                                edit = ps.baseButtonGroup([
                                                        ps.baseAButton(ps.baseIcon("zoom-in"),
                                                                classes="",
                                                                link=c.baseURL+"/post/"+post.id,
                                                                data=[("original-title", "Expand Post")],
                                                                rel="tooltip"),
                                                        ])
 
                                        content += ps.baseRow(ps.baseColumn(ps.baseAnchor(ps.baseHeading(post.title, size=1), link=c.baseURL+"/post/"+post.id)))
                                        content += ps.baseRow(ps.baseColumn(ps.baseWell(
                                                        ps.baseColumn(ps.baseBold("Author: ", classes="muted"))+
                                                        ps.baseColumn(post.author)+
                                                        ps.baseColumn(ps.baseBold("When: ", classes="muted"))+
                                                        ps.baseColumn(post.time)+
                                                        ps.baseColumn(edit, classes="pull-right")
                                                        ), width=10
                                                ))

                                        content += ps.baseRow([
                                                ps.baseColumn(ps.baseParagraph(post["post"][:250]+ps.baseAnchor("...", link=c.baseURL+"/post/"+post.id))),
                                                ])
                                        content += "<hr>"

                if not content:
                        content = "We don't have any news to bring you just this moment, however stay tuned!"


                self.view.body = hero + content
                self.view.scripts = ps.baseScript("""
        $('#frontCarousel').carousel()
                """)


@route("/post/(.*)")
@route("/posts/view/(.*)")
class postsView(basePage):
        def GET(self):
                """
                """
                post = pm.post(self.members[0], True)

                self.view["title"] = "Post: %s" % post.title

                content = ""

                if not c.session.user["level"] in ["admin", "GOD"]:
                        other = ""
                else:
                        other = ps.baseColumn(
                                ps.baseButtonGroup([
                                ps.baseAButton(ps.baseIcon("edit"),
                                        classes="btn-info",
                                        link=c.baseURL+"/admin/post/%s/edit"%post.id,
                                        data=[("original-title", "Edit Post")],
                                        rel="tooltip"),
                                ps.baseAButton(ps.baseIcon("trash"),
                                        classes="btn-danger",
                                        link=c.baseURL+"/admin/post/%s/delete"%post.id,
                                        data=[("original-title", "Delete Post")],
                                        rel="tooltip")
                                        ])
                                )


                content += ps.baseRow(ps.baseColumn(ps.baseHeading(post.title, size=1)))
                content += ps.baseRow(ps.baseColumn(ps.baseWell(
                        ps.baseColumn(ps.baseBold("Author: ", classes="muted"))+
                        ps.baseColumn(post.author)+
                        ps.baseColumn(ps.baseBold("When: ", classes="muted"))+
                        ps.baseColumn(post.time)+
                        ps.baseColumn(other, classes="pull-right")
                        ), width=10
                        ))
                content += ps.baseRow([
                        ps.baseColumn(ps.baseParagraph(post["post"])),
                        ])

                self.view["body"] = content
