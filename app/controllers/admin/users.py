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
from seshat.route import route

import models.basic.authModel as am

import views.pyStrap.pyStrap as ps

@route("/admin/users")
class usersIndex_admin(basePage):
        __menu__ = "Users"
        def GET(self):
                """

                """
                users = am.userList()

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Users" % ps.baseIcon("group"), size=1)),
                                ps.baseButtonGroup([
                                        ps.baseAButton(ps.baseIcon("magic"), link=c.baseURL+"/admin/users/new",
                                        data=[("original-title", "New User")],
                                        rel="tooltip",
                                        classes="btn-info")
                                ], classes="pull-right")
                        ]) + "<hr>"


                if users:
                        content = ""
                        for user in users:
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseHeading("Name: " + user.username, size=5), width=4),
                                        ps.baseColumn(ps.baseParagraph("Level: "+ user.level), width=4)
                                        ])
                                editButton = ps.baseAButton(ps.baseIcon("edit"),
                                                classes="btn-info",
                                                link=c.baseURL+"/admin/users/edit/%s"%user.id,
                                                data=[("original-title", "Edit User")],
                                                rel="tooltip")
                                deleteButton = ps.baseAButton(ps.baseIcon("trash"),
                                                classes="btn-danger",
                                                link=c.baseURL+"/admin/users/delete/%s"%user.id,
                                                data=[("original-title", "Delete User")],
                                                rel="tooltip")
                                actions = ps.baseButtonGroup([editButton, deleteButton])
                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseParagraph("Notes: "+user.notes), width=6),
                                        ps.baseColumn(actions, width=2)
                                        ])
                                content += "<hr>"
                else:
                        content = "Well either all of your users have god perms and aren't shown, or you don't have any additional users!"

                self.view["body"] = pageHead + content
                self.view.scripts = ps.baseScript("""
                $('.btn-group').tooltip({
                      selector: "a[rel=tooltip]"
                })
""")
@route("/admin/users/edit/(.*)")
class usersEdit_admin(basePage):
        def GET(self):
                """
                """
                id = self.members[0]
                user = am.baseUser(id)

                self.view["title"] = "Edit User " + user.username
                pageHead = ps.baseHeading("%s Editing user: %s" % (ps.baseIcon("group"), user.username), size=1)

                other = [{"label": "Default/Normal", "value": "normal"},
                        {"label": "Admin", "value": "admin"}]

                if user.level == "admin":
                        other = [{"label": "Default/Normal", "value": "normal"},
                                {"label": "Admin", "value": "admin", "selected": ""}]


                if c.session.user.level == "GOD":
                        if user.level == "GOD":
                                other.append({"label": "Demigod", "value": "god", "selected": ""})
                        else:
                                other.append({"label": "Demigod", "value": "god"})

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/admin/users/edit/" + id),
                        method="POST",
                        actions=[ps.baseButtonGroup([ps.baseSubmit("Update, perhaps?", classes="btn-info"), ps.baseAButton("Delete, perhaps?", classes="btn-danger", link=c.baseURL+"/admin/users/delete/"+user.id)])],
                        fields=[
                                {"label": "Set a new Password, perhaps?", "content": ps.baseInput(type="password", name="password", placeholder="password", classes="span5")},
                                {"label": "Add a note to their account, perhaps?", "content": ps.baseTextarea(user.notes, name="notes", classes="span5")},
                                {"label": "User level", "content": ps.baseSelect(elements=other, classes="span5", name="level")}
                                ]
                       )

                self.view["body"] = pageHead + editForm

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

                        user.level = self.members["level"]

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
                pageHead = ps.baseHeading("%s Delete user: %s" % (ps.baseIcon("group"), user.username), size=1, classes="text-error")

                confirm = ps.baseHeading("Are you sure?", size = 1, classes="text-error")
                confirm += ps.baseParagraph("You are about to delete user: %s"%user.username, classes="text-error")
                confirm += ps.baseParagraph("Pressing confirm will delete this user forever and you will not be able to recover them. Are you sure you would like to continue?", classes="text-warning")

                confirmForm = ps.baseBasicForm(action=c.baseURL+"/admin/users/delete/"+user.id,
                                method="POST",
                                fields=[ps.baseButtonGroup([ps.baseSubmit("I feel no mercy (Delete)", classes="btn-danger"), ps.baseAButton("NO, I made a mistake!(Don't Delete)", link=c.baseURL+"/admin/users/edit/"+user.id, classes="btn-info")])])

                confirm += ps.baseWell(confirmForm)

                self.view.body=pageHead+confirm

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
                pageHead = ps.baseHeading("%s Creating a new user" % ps.baseIcon("group"), size=1)

                other = [{"label": "Default/Normal", "value": "normal"},
                        {"label": "Admin", "value": "admin"},
                        {"label": "Demigod", "value": "god"}]

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/admin/users/new"),
                        method="POST",
                        actions=[ps.baseSubmit(content="MAKE ME!", classes="btn-info")],
                        fields=[
                                {"label": "Imaginary Friend?", "content": ps.baseInput(type="text", name="username", placeholder="username", classes="span5")},
                                {"label": "Password?", "content": ps.baseInput(type="password", name="password", placeholder="Password", classes="span5")},
                                {"label": "How about: add a note to their account?", "content": ps.baseTextarea(name="notes", classes="span5")},
                                {"label": "User level", "content": ps.baseSelect(elements=other, classes="span5", name="level")}
                                ]
                       )

                self.view.body = pageHead + editForm

        def POST(self):
                """

                """
                name = self.members["username"]
                notes = self.members["notes"] or ""
                try:
                        user = am.baseUser()
                        user["username"] = name
                        user["notes"] = notes
                        user.level = self.members["level"]
                        user.password = self.members["password"]

                        user.commit()

                        self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                        c.session.pushMessage(("The user %s was created!" % ps.baseBold(user.username)), title="Congratulations!", icon="ok", type="success")

                except Exception as exc:
                        if c.debug: print exc
                        self.head = ("303 SEE OTHER", [("location", "/admin/users/new")])
                        c.session.pushMessage("Something went wrong while creating the user: %s. Heres the edit form again. Sorry!" % ps.baseBold(name), icon="fire", title="OH SNAP!", type="error")

