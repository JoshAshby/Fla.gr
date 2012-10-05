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

from objects.adminObject import adminObject as basePage
from objects.userObject import userObject as setupPage
from seshat.route import route

import models.basic.authModel as am
import models.basic.postModel as pm

import views.pyStrap.pyStrap as ps


@route("/admin")
class adminIndex_admin(basePage):
        __menu__ = "Admin Panel"
        def GET(self):
                """
                """

                hero = ps.baseHeading(ps.baseIcon("dashboard") + " Howdy, Admin!", size=1)
                hero += ps.baseParagraph("This is the admin panel. Here you can manage aspects of the site such as users, front page posts and sometime later, even more!")

                self.view["body"] = ps.baseHero(hero) + ps.baseParagraph("Well you have nothing to do here at the moment, but you might want to take a look over at the sidebar for somethings to do...")


@route("/admin/users")
class usersIndex_admin(basePage):
        __menu__ = "Users"
        def GET(self):
                """

                """
                users = am.userList()

                pageHead = """
                %s <br>
                <hr>
                """ % ps.baseAButton("Add a user", classes="btn-info", link=c.baseURL + "/admin/users/new")


                if users:
                        content = ""
                        for user in users:
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseHeading("Name: " + user.username, size=5), width=4),
                                        ps.baseColumn(ps.baseParagraph("Level: "+ user.level), width=4)
                                        ])
                                editButton = ps.baseAButton("Edit", classes="btn-info", link=c.baseURL+"/admin/users/edit/%s"%user.id)
                                deleteButton = ps.baseAButton("Delete", classes="btn-danger", link=c.baseURL+"/admin/users/delete/%s"%user.id)
                                actions = ps.baseButtonGroup([editButton, deleteButton])
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseParagraph("Notes: "+user.notes), width=6),
                                        ps.baseColumn(actions, width=2)
                                        ])
                                content += "<hr>"
                else:
                        content = "Well either all of your users have god perms and aren't shown, or you don't have any additional users!"

                self.view["body"] = pageHead + content


@route("/admin/users/edit/(.*)")
class usersEdit_admin(basePage):
        def GET(self):
                """
                """
                id = self.members[0]
                user = am.baseUser(id)

                self.view["title"] = "Edit User " + user.username

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/admin/users/edit/" + id),
                        method="POST",
                        actions=[ps.baseButtonGroup([ps.baseSubmit("Update, perhaps?", classes="btn-info"), ps.baseAButton("Delete, perhaps?", classes="btn-danger", link=c.baseURL+"/admin/users/delete/"+user.id)])],
                        fields=[
                                {"label": "Set a new Password, perhaps?", "content": ps.baseInput(type="password", name="password", placeholder="password", classes="span5")},
                                {"label": "Add a note to their account, perhaps?", "content": ps.baseTextarea(user.notes, name="notes", classes="span5")}
                                ]
                       )

                self.view["body"] = ps.baseHeading("Editing user: %s" % ps.baseSmall(user.username), size=2) + editForm

        def POST(self):
                """
                """
                id = self.members[0]
                notes = self.members["notes"] or ""

                try:
                        user = am.baseUser(id)
                        user["notes"] = notes

                        if self.members["password"]:
                                user.password = self.members["password"]

                        user.commit()

                        self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                        c.session.pushMessage(("The user %s was updated!" % ps.baseBold(user.username)), title="Congratulations!", icon="ok", type="success")

                except Exception as exc:
                        self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                        c.session.pushMessage("Something went wrong while updateing the user, id: %s. Heres the edit form again. Sorry!" % ps.baseBold(user.id), icon="fire", title="OH SNAP!", type="error")


@route("/admin/users/delete/(.*)")
class usersDelete_admin(basePage):
        def GET(self):
                id = self.members[0]
                user = am.baseUser(id)

                self.view.title = "Delete user %s" % user.username

                confirm = ps.baseHeading("Are you sure?", size = 1, classes="text-error")
                confirm += ps.baseParagraph("You are about to delete user: %s"%user.username, classes="text-error")
                confirm += ps.baseParagraph("Pressing confirm will delete this user forever and you will not be able to recover them. Are you sure you would like to continue?", classes="text-warning")

                confirmForm = ps.baseBasicForm(action=c.baseURL+"/admin/users/delete/"+user.id,
                                method="POST",
                                fields=[ps.baseButtonGroup([ps.baseSubmit("I feel no mercy (Delete)", classes="btn-danger"), ps.baseAButton("NO, I made a mistake!(Don't Delete)", link=c.baseURL+"/admin/users/edit/"+user.id, classes="btn-info")])])

                confirm += ps.baseWell(confirmForm)

                self.view.body=confirm

        def POST(self):
                id = self.members[0]
                user = am.baseUser(id)

                user.delete()

                self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                c.session.pushMessage(("The user %s was deleted" % ps.baseBold(user.username)), title="Bye!", icon="trash", type="error")


@route("/admin/users/new")
class usersNew_admin(basePage):
        def GET(self):
                """
                This gives a nice little list of all the users in the system, 
                with the exception of users marked as having GOD level.
                """
                self.view["title"] = "Create a new user"

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/admin/users/new"),
                        method="POST",
                        actions=[ps.baseSubmit(content="MAKE ME!", classes="btn-info")],
                        fields=[
                                {"label": "Imaginary Friend?", "content": ps.baseInput(type="text", name="username", placeholder="username", classes="span5")},
                                {"label": "Password?", "content": ps.baseInput(type="password", name="password", placeholder="Password", classes="span5")},
                                {"label": "How about: add a note to their account?", "content": ps.baseTextarea(name="notes", classes="span5")}
                                ]
                       )

                self.view.body = editForm

        def POST(self):
                """

                """
                name = self.members["username"]
                notes = self.members["notes"] or ""
                try:
                        user = am.baseUser()
                        user["username"] = name
                        user["notes"] = notes
                        user.password = self.members["password"]

                        user.commit()

                        self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                        c.session.pushMessage(("The user %s was created!" % ps.baseBold(user.username)), title="Congratulations!", icon="ok", type="success")

                except Exception as exc:
                        self.head = ("303 SEE OTHER", [("location", "/admin/users/new")])
                        c.session.pushMessage("Something went wrong while creating the user: %s. Heres the edit form again. Sorry!" % ps.baseBold(name), icon="fire", title="OH SNAP!", type="error")


@route("/admin/posts")
class postsIndex_admin(basePage):
        def GET(self):
                """
                """
                posts = pm.postList()

                self.view["title"] = "Posts"

                pageHead = """
                %s <br>
                <hr>
                """ % ps.baseAButton(classes="btn-info", content="Add a new post", link=c.baseURL + "/admin/posts/new")


                if posts:
                        content = ""
                        for post in posts:
                                content += ps.baseRow([ps.baseColumn(ps.baseHeading(post.title, size=3), width=8)])
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseHeading("Author: " + post.author, size=6, classes="muted"), width=4),
                                        ps.baseColumn(ps.baseParagraph("When: "+ post.time), width=4)
                                        ])
                                editButton = ps.baseAButton("Edit", classes="btn-info", link=c.baseURL+"/admin/posts/edit/%s"%post.id)
                                deleteButton = ps.baseAButton("Delete", classes="btn-danger", link=c.baseURL+"/admin/posts/delete/%s"%post.id)
                                actions = ps.baseButtonGroup([editButton, deleteButton])
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseParagraph("Post: "+post.post), width=6),
                                        ps.baseColumn(actions, width=2)
                                        ])
                                content += "<hr>"
                else:
                        content = "You don't have any posts! Why don't you make one?"

                self.view["body"] = pageHead + content


@route("/admin/posts/edit/(.*)")
class postsEdit_admin(basePage):
        def GET(self):
                """
                """
                id = self.members[0]

                post = pm.basePost(id)

                self.view["title"] = "Update post "+post.title

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/admin/posts/edit/"+post.id),
                        method="POST",
                        actions=[ps.baseButtonGroup([ps.baseSubmit("Update", classes="btn-info"),
                                ps.baseAButton("Delete", link=c.baseURL+"/admin/posts/delete/"+post.id, classes="btn-danger")])],
                        fields=[
                                {"label": "What should my title be, hmm?", "content": ps.baseInput(type="text", name="title", value=post.title, classes="span5")},
                                {"label": "Why don't you write something fancy? (markdown enabled)", "content": ps.baseTextarea(name="post", classes="span5", content=post.post)}
                                ]
                       )

                self.view["body"] = editForm

        def POST(self):
                """
                """
                id = self.members[0]
                title = self.members["title"]
                post = self.members["post"]

                updatePost = pm.basePost(id)

                updatePost["title"] = title
                updatePost["post"] = post
                updatePost["author"] = c.session.user.username

                updatePost.commit()

                self.head = ("303 SEE OTHER", [("location", "/admin/posts")])
                c.session.pushMessage(("The post %s was updated!" % ps.baseBold(title)), title="Congratulations!", icon="ok", type="success")


@route("/admin/posts/delete/(.*)")
class postsDelete_admin(basePage):
        def GET(self):
                id = self.members[0]
                post = pm.basePost(id)

                self.view.title = "Delete post %s" % post.title

                confirm = ps.baseHeading("Are you sure?", size = 1, classes="text-error")
                confirm += ps.baseParagraph("You are about to delete the post: %s" % post.title, classes="text-error")
                confirm += ps.baseParagraph("Pressing confirm will delete this post forever and you will not be able to recover it. Are you sure you would like to continue?")

                confirmForm = ps.baseBasicForm(action=c.baseURL+"/admin/posts/delete/"+post.id,
                                method="POST",
                                fields=[ps.baseButtonGroup([ps.baseSubmit("Yes, I am sure.", classes="btn-danger"), ps.baseAButton("NO, Do Not Delete!", link=c.baseURL+"/admin/posts/edit/"+post.id, classes="btn-info")])])

                confirm += ps.baseWell(confirmForm)

                self.view.body=confirm

        def POST(self):
                id = self.members[0]
                post = pm.basePost(id)

                post.delete()

                self.head = ("303 SEE OTHER", [("location", "/admin/posts")])
                c.session.pushMessage(("The post %s was deleted" % ps.baseBold(post.title)), title="Bye Bye", icon="trash", type="error")


@route("/admin/posts/new")
class postsNew_admin(basePage):
        def GET(self):
                """
                """
                self.view["title"] = "Create a new post"

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/admin/posts/new"),
                        method="POST",
                        actions=[ps.baseSubmit("MAKE ME A POST!", classes="btn-info")],
                        fields=[
                                {"label": "What should my title be, hmm?", "content": ps.baseInput(type="text", name="title", placeholder="title", classes="span5")},
                                {"label": "Why don't you write something fancy? (markdown enabled)", "content": ps.baseTextarea(name="post", classes="span5")}
                                ]
                       )

                self.view["body"] = editForm

        def POST(self):
                """
                """
                title = self.members["title"]
                post = self.members["post"]

                newPost = pm.basePost()

                newPost["title"] = title
                newPost["post"] = post
                newPost["author"] = c.session.user.username

                newPost.commit()

                self.head = ("303 SEE OTHER", [("location", "/admin/posts")])
                c.session.pushMessage(("Congrats! The post %s was created!" % ps.baseBold(title)), title="Congratulations!", icon="ok", type="success")
