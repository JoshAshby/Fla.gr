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

from flagr.objects.adminObject import adminObject
from seshat.route import route

import flagr.models.postModel as pm
import flagr.views.pyStrap.pyStrap as ps


@route("/admin/posts")
class postsIndex_admin(adminObject):
        def GET(self):
                """
                """
                posts = pm.postList(md=True)

                self.view["title"] = "Posts"

                tabs = "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("rss"), link=c.baseURL+"/admin/posts",
                                rel="tooltip",
                                data=[("original-title", "All Posts"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("wrench"), link=c.baseURL+"/admin/posts/drafts",
                                rel="tooltip",
                                data=[("original-title", "Draft Posts"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += ps.baseButtonGroup([
                        ps.baseAButton(ps.baseIcon("magic"), link=c.baseURL+"/admin/posts/new",
                        data=[("original-title", "New Post"),
                                ("placement", "bottom")],
                        rel="tooltip",
                        classes="btn-info")
                        ], classes="pull-right")


                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Blog Posts" % (ps.baseIcon("rss")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=3)
                        ])

                if posts:
                        content = ""
                        for post in posts:
                                if not post["visibility"]:
                                        other = ps.baseAnchor(ps.baseLabel("%s Draft" % ps.baseIcon("eye-close")), link=c.baseURL+"/admin/posts/drafts")
                                else:
                                        other = ps.baseLabel("%s Published" % ps.baseIcon("globe"))

                                edit = ps.baseSplitDropdown(btn=ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                        classes="", link=c.baseURL+"/admin/post/%s"%post.id,
                                        rel="tooltip",
                                        data=[("original-title", "Expand")]),
                                        dropdown=ps.baseMenu(name="postDropdown",
                                                items=[{"name": "%s Edit" % ps.baseIcon("edit"), "link": c.baseURL+"/admin/post/%s/edit"%post.id},
                                                        {"name": ps.baseBold("%s Delete" % ps.baseIcon("trash"), classes="text-error"), "link": c.baseURL+"/admin/post/%s/delete"%post.id}]
                                                ),
                                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                                classes="dropdown-toggle btn-danger",
                                                data=[("toggle", "dropdown"),
                                                        ("original-title", "Edit Options")],
                                                rel="tooltip"))

                                content += ps.baseRow(ps.baseColumn(ps.baseHeading(post.title, size=3)))
                                content += ps.baseRow(ps.baseColumn(ps.baseWell(
                                        ps.baseColumn(ps.baseBold("Author: ", classes="muted"))+
                                        ps.baseColumn(post.author)+
                                        ps.baseColumn(ps.baseBold("When: ", classes="muted"))+
                                        ps.baseColumn(post.time)+
                                        ps.baseColumn(other)+
                                        ps.baseColumn(edit, classes="pull-right", width=1)
                                        ), width=8
                                ))
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseParagraph(post["post"][:250]+ps.baseAnchor("...", link=c.baseURL+"/admin/post/%s"%post.id))),
                                        ])
                                content += "<hr>"
                else:
                        content = "You don't have any posts! Why don't you make one?"

                self.view["body"] = pageHead + content


@route("/admin/posts/drafts")
class postsDrafts_admin(adminObject):
        def GET(self):
                """
                """
                posts = pm.postList(md=True)

                self.view["title"] = "Posts"

                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("rss"), link=c.baseURL+"/admin/posts",
                                rel="tooltip",
                                data=[("original-title", "All Posts"),
                                        ("placement", "bottom")]) +"</li>"
                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("wrench"), link=c.baseURL+"/admin/posts/drafts",
                                rel="tooltip",
                                data=[("original-title", "Draft Posts"),
                                        ("placement", "bottom")]) +"</li>"

                tabs += ps.baseButtonGroup([
                        ps.baseAButton(ps.baseIcon("magic"), link=c.baseURL+"/admin/posts/new",
                        data=[("original-title", "New Post"),
                                ("placement", "bottom")],
                        rel="tooltip",
                        classes="btn-info")
                        ], classes="pull-right")


                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Blog Drafts" % (ps.baseIcon("rss")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=3)
                        ])

                content = ""
                for post in posts:
                        if not post["visibility"]:
                                other = ps.baseAnchor(ps.baseLabel("%s Draft" % ps.baseIcon("eye-close")), link=c.baseURL+"/admin/posts/drafts")
                                edit = ps.baseSplitDropdown(btn=ps.baseAButton("%s" % ps.baseIcon("zoom-in"),
                                        classes="", link=c.baseURL+"/admin/post/%s/view"%post.id,
                                        rel="tooltip",
                                        data=[("original-title", "Expand")]),
                                        dropdown=ps.baseMenu(name="postDropdown",
                                                items=[{"name": "%s Edit" % ps.baseIcon("edit"), "link": c.baseURL+"/admin/post/%s/edit"%post.id},
                                                        {"name": ps.baseBold("%s Delete" % ps.baseIcon("trash"), classes="text-error"), "link": c.baseURL+"/admin/post/%s/delete"%post.id}]
                                                ),
                                        dropBtn=ps.baseAButton("""<i class="icon-chevron-down"></i>""",
                                                classes="dropdown-toggle btn-danger",
                                                data=[("toggle", "dropdown"),
                                                        ("original-title", "Edit Options")],
                                                rel="tooltip"))

                                content += ps.baseRow(ps.baseColumn(ps.baseHeading(post.title, size=3)))
                                content += ps.baseRow(ps.baseColumn(ps.baseWell(
                                        ps.baseColumn(ps.baseBold("Author: ", classes="muted"))+
                                        ps.baseColumn(post.author)+
                                        ps.baseColumn(ps.baseBold("When: ", classes="muted"))+
                                        ps.baseColumn(post.time)+
                                        ps.baseColumn(other)+
                                        ps.baseColumn(edit, classes="pull-right")
                                        ), width=8
                                ))
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseParagraph(post["post"][:250]+ps.baseAnchor("...", link=c.baseURL+"/admin/post/%s"%post.id))),
                                        ])
                                content += "<hr>"
                if not content:
                        content = "You don't have any draft posts! Why don't you make one?"

                self.view["body"] = pageHead + content


@route("/admin/post/(.*)/edit")
class postsEdit_admin(adminObject):
        def GET(self):
                post = pm.post(self.members[0])

                self.view.title = "Editing post: %s" % post.title

                elements = [
                ps.baseInput(type="text", classes="span8", name="title", value=post["title"], placeholder="Title"),
                "<br /><br />",
                {"content": ps.baseTextarea(classes="span8", name="post", content=post["post"]),
                        "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"), classes="muted")},
                "<br />",
                {"label": "Publish?",
                        "content": ps.baseCheckbox(name="visibility", checked=post["visibility"],
                        label="If you want the rest of the world to be able to see this post, mark the checkbox. If not, leave it unchecked to mark as a draft.")},
                        ]


                editForm = ps.baseHeading("%s Editing post: %s" % (ps.baseIcon("rss"), post["title"]), size=1)
                editForm += ps.baseHorizontalForm(action=c.baseURL+"/admin/post/%s/edit"% (self.members[0]),
                                method="POST",
                                actions=[ps.baseSubmit(ps.baseIcon("save")+" Update!")],
                                fields=elements)

                self.view.body = editForm


        def POST(self):
                post = pm.post(self.members[0])

                if not self.members.has_key("visibility"): self.members["visibility"] = False

                for field in post.fields:
                        part = field[0].lower() if type(field) != str else field.lower()
                        if self.members.has_key(part):
                                post[part] = self.members[part]

                post.commit()
                self.head = ("303 SEE OTHER", [("location", str("/admin/post/"+post.id))])
                c.session.pushAlert(("You updated post: %s!" % ps.baseBold(post.title)), type="success", icon="ok", title="YAY!")


@route("/admin/post/(.*)/delete")
class postsDelete_admin(adminObject):
        def GET(self):
                id = self.members[0]
                post = pm.post(id)

                self.view.title = "Delete post %s" % post.title

                confirm = ps.baseHeading("Are you sure?", size = 1, classes="text-error")
                confirm += ps.baseParagraph("You are about to delete the post: %s" % post.title, classes="text-error")
                confirm += ps.baseParagraph("Pressing confirm will delete this post forever and you will not be able to recover it. Are you sure you would like to continue?")

                confirmForm = ps.baseBasicForm(action=c.baseURL+"/admin/post/%s/delete"%post.id,
                                method="POST",
                                fields=[ps.baseButtonGroup([ps.baseSubmit("Yes, I am sure.", classes="btn-danger"), ps.baseAButton("NO, Do Not Delete!", link=c.baseURL+"/admin/post/%s/edit"%post.id, classes="btn-info")])])

                confirm += ps.baseWell(confirmForm)

                self.view.body=confirm

        def POST(self):
                id = self.members[0]
                post = pm.post(id)

                post.delete()

                self.head = ("303 SEE OTHER", [("location", "/admin/posts")])
                c.session.pushAlert(("The post %s was deleted" % ps.baseBold(post.title)), title="Bye Bye", icon="trash", type="error")


@route("/admin/posts/new")
class postsNew_admin(adminObject):
        def GET(self):
                self.view.title = "Creating a new post"
                title = ps.baseHeading("%s Creating a new post..." % (ps.baseIcon("rss")), size=1)

                elements = [
                ps.baseInput(type="text", classes="span8", name="title", placeholder="Title"),
                "<br /><br />",
                {"content": ps.baseTextarea(classes="span8", name="post"),
                        "help": ps.baseSmall("Text can be formated with %s" % ps.baseAnchor("Daring Fireball's Markdown", link="http://daringfireball.net/projects/markdown/syntax"), classes="muted")},
                "<br />",
                {"label": "Publish?",
                        "content": ps.baseCheckbox(name="visibility",
                        label="If you want the rest of the world to be able to see this post, mark the checkbox. If not, leave it unchecked to mark as a draft.")},
                        ]


                editForm = ps.baseHeading("%s Creating a new post" % (ps.baseIcon("rss")), size=1)
                editForm += ps.baseHorizontalForm(action=c.baseURL+"/admin/posts/new",
                                method="POST",
                                actions=[ps.baseSubmit(ps.baseIcon("save")+" Create!")],
                                fields=elements)

                self.view.body = editForm


        def POST(self):
                post = pm.post()

                if not self.members.has_key("visibility"): self.members["visibility"] = False

                for field in post.fields:
                        part = field[0].lower() if type(field) != str else field.lower()
                        if self.members.has_key(part):
                                post[part] = self.members[part]

                post.commit()
                self.head = ("303 SEE OTHER", [("location", str("/admin/post/%s"%post.id))])
                c.session.pushAlert(("You created post: %s!" % ps.baseBold(post.title)), type="success", icon="ok", title="YAY!")


@route("/admin/post/(.*)")
@route("/admin/post/(.*)/view")
class postsView_admin(adminObject):
        def GET(self):
                """
                """
                post = pm.post(self.members[0], True)

                self.view["title"] = "Post: %s" % post.title
                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Viewing post: %s" % (ps.baseIcon("rss"), post["title"]), size=1))
                        ]) + "<hr>"

                content = ""

                if not post["visibility"]:
                        other = ps.baseAnchor(ps.baseLabel("%s Draft" % ps.baseIcon("eye-close")), link=c.baseURL+"/admin/posts/drafts")
                else:
                        other = ps.baseLabel("%s Published" % ps.baseIcon("globe"))

                content += ps.baseRow(ps.baseColumn(ps.baseHeading(post.title, size=1)))
                content += ps.baseRow(ps.baseColumn(ps.baseWell(
                        ps.baseColumn(ps.baseBold("Author: ", classes="muted"))+
                        ps.baseColumn(post.author)+
                        ps.baseColumn(ps.baseBold("When: ", classes="muted"))+
                        ps.baseColumn(post.time)+
                        ps.baseColumn(other)+
                        ps.baseColumn(
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
                                        ]), classes="pull-right"
                                )
                        ), width=8
                ))
                content += ps.baseRow([
                        ps.baseColumn(ps.baseParagraph(post["post"])),
                        ])

                self.view["body"] = pageHead + content
