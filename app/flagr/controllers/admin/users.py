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

import flagr.views.pyStrap.pyStrap as ps
import models.profileModel as profilem


@route("/admin/users")
class usersIndex_admin(adminObject):
        __menu__ = "Users"
        def GET(self):
                """

                """
                users = profilem.userList()

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
                                if user["disable"]:
                                        dis = ps.baseLabel("%s Disabled" % ps.baseIcon("ban-circle"))
                                else:
                                        dis = ps.baseLabel("%s Active" % ps.baseIcon("ok-circle"))

                                editButton = ps.baseAButton(ps.baseIcon("edit"),
                                                classes="btn-info",
                                                link=c.baseURL+"/admin/user/%s/edit"%user.id,
                                                data=[("original-title", "Edit User")],
                                                rel="tooltip")
                                deleteButton = ps.baseAButton(ps.baseIcon("trash"),
                                                classes="btn-danger",
                                                link=c.baseURL+"/admin/user/%s/delete"%user.id,
                                                data=[("original-title", "Delete User")],
                                                rel="tooltip")
                                actions = ps.baseButtonGroup([editButton, deleteButton])

                                content += ps.baseRow(ps.baseColumn(ps.baseWell(
                                        ps.baseColumn(ps.baseBold("Username:", classes="muted")) +
                                        ps.baseColumn(
                                                ps.baseAnchor(user["username"], link=c.baseURL+"/people/%s"%user["username"])) +
                                        ps.baseColumn(ps.baseBold("Level:", classes="muted")) +
                                        ps.baseColumn(user["level"]) +
                                        ps.baseColumn(dis) +
                                        ps.baseColumn(actions, classes="pull-right")
                                        ), width=8))

                                content += ps.baseRow([
                                        ps.baseColumn(ps.baseParagraph("Notes: "+user["adminNotes"]), width=8)
                                        ])
                                content += "<hr>"
                else:
                        content = "Uh, well this is bad... unless you don't have god permissions and can't see any of the deities..."

                self.view["body"] = pageHead + content


@route("/admin/user/(.*)/edit")
class usersEdit_admin(adminObject):
        def GET(self):
                """
                """
                id = self.members[0]
                user = profilem.profile(id, md=False)

                self.view["title"] = "Edit User " + user["username"]
                pageHead = ps.baseHeading("%s Editing user: %s" % (ps.baseIcon("group"), user["username"]), size=1)

                other = [{"label": "Default/Normal", "value": "normal"},
                        {"label": "Admin", "value": "admin"}]

                if user.level == "admin":
                        other = [{"label": "Default/Normal", "value": "normal"},
                                {"label": "Admin", "value": "admin", "selected": ""}]


                if c.session.user["level"] == "GOD":
                        if user["level"] == "GOD":
                                other.append({"label": "Demigod", "value": "GOD", "selected": ""})
                        else:
                                other.append({"label": "Demigod", "value": "GOD"})

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/admin/user/%s/edit" % id),
                        method="POST",
                        actions=[ps.baseButtonGroup([ps.baseSubmit("Update, perhaps?", classes="btn-info"), ps.baseAButton("Delete, perhaps?", classes="btn-danger", link=c.baseURL+"/admin/user/%s/delete"%user.id)])],
                        fields=[ps.baseHeading("Admin stuff...", size=3), "<hr>",
                                {"label": "Set a new Password, perhaps?", "content": ps.baseInput(type="password", name="password", placeholder="password", classes="span5")},
                                {"label": "Add a note to their account, perhaps?", "content": ps.baseTextarea(user["adminNotes"], name="notes", classes="span5")},
                                {"label": "User level", "content": ps.baseSelect(elements=other, classes="span5", name="level")},
                                {"label": "Disable/Ban?", "content": ps.baseCheckbox(name="disable", checked=user["disable"], label="Check to disable/ban the user")},
                                ps.baseHeading("Profile stuff...", size=3), "<hr>",
                                {"label": "Profile Visibility", "content": ps.baseCheckbox(name="visibility", checked=user["visibility"], label="Users public profile visibility. Checked for visibile")},
                                {"label": "About", "content": ps.baseTextarea(user["about"], name="about", classes="span5")},
                                {"label": "Email", "content": ps.baseInput(type="email", name="email", placeholder="email@email.com", classes="span5", content=user["email"])},
                                {"label": "Email Visibility", "content": ps.baseCheckbox(name="emailVisibility", checked=user["emailVisibility"], label="Users email visibility. Checked for visibile")},
                                ]
                       )

                self.view["body"] = pageHead + editForm

        def POST(self):
                """
                """
                id = self.members[0]
                notes = self.members["notes"] or ""
                if not self.members.has_key("disable"): self.members["disable"] = False
                if not self.members.has_key("visibility"): self.members["visibility"] = False
                if not self.members.has_key("emailVisibility"): self.members["emailVisibility"] = False

                try:
                        user = profilem.profile(id)
                        user["adminNotes"] = notes

                        if self.members["password"]:
                                user["password"] = self.members["password"]

                        user["level"] = self.members["level"]
                        user["disable"] = self.members["disable"]
                        user["visibility"] = self.members["visibility"]
                        user["emailVisibility"] = self.members["emailVisibility"]
                        user["about"] = self.members["about"]
                        user["email"] = self.members["email"]

                        user.commit()

                        self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                        c.session.pushAlert(("The user %s was updated!" % ps.baseBold(user["username"])), title="Congratulations!", icon="ok", type="success")

                except Exception as exc:
                        self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                        c.session.pushAlert("Something went wrong while updateing the user, id: %s. Heres the edit form again. Sorry!" % ps.baseBold(user.id), icon="fire", title="OH SNAP!", type="error")


@route("/admin/user/(.*)/delete")
class usersDelete_admin(adminObject):
        def GET(self):
                id = self.members[0]
                user = profilem.profile(id)

                self.view.title = "Delete user %s" % user.username
                pageHead = ps.baseHeading("%s Delete user: %s" % (ps.baseIcon("group"), user.username), size=1, classes="text-error")

                confirm = ps.baseHeading("Are you sure?", size = 1, classes="text-error")
                confirm += ps.baseParagraph("You are about to delete user: %s"%user.username, classes="text-error")
                confirm += ps.baseParagraph("Pressing confirm will delete this user forever and you will not be able to recover them. Are you sure you would like to continue?", classes="text-warning")

                confirmForm = ps.baseBasicForm(action=c.baseURL+"/admin/user/%s/delete"%user.id,
                                method="POST",
                                fields=[ps.baseButtonGroup([ps.baseSubmit("I feel no mercy (Delete)", classes="btn-danger"), ps.baseAButton("NO, I made a mistake!(Don't Delete)", link=c.baseURL+"/admin/user/%s/edit"%user.id, classes="btn-info")])])

                confirm += ps.baseWell(confirmForm)

                self.view.body=pageHead+confirm

        def POST(self):
                id = self.members[0]
                user = profilem.profile(id)

                user.delete()

                self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                c.session.pushAlert(("The user %s was deleted" % ps.baseBold(user["username"])), title="Bye!", icon="trash", type="error")


@route("/admin/users/new")
class usersNew_admin(adminObject):
        def GET(self):
                """
                This gives a nice little list of all the users in the system, 
                with the exception of users marked as having GOD level.
                """
                self.view["title"] = "Create a new user"
                pageHead = ps.baseHeading("%s Creating a new user" % ps.baseIcon("group"), size=1)

                other = [{"label": "Default/Normal", "value": "normal"},
                        {"label": "Admin", "value": "admin"}]


                if c.session.user["level"] == "GOD":
                        other.append({"label": "Demigod", "value": "GOD"})

                editForm = ps.baseHorizontalForm(action=(c.baseURL+"/admin/users/new"),
                        method="POST",
                        actions=[ps.baseSubmit(content="MAKE ME!", classes="btn-info")],
                        fields=[ps.baseHeading("Admin stuff...", size=3), "<hr>",
                                {"label": "Imaginary Friend?", "content": ps.baseInput(type="text", name="username", placeholder="username", classes="span5")},
                                {"label": "Password?", "content": ps.baseInput(type="password", name="password", placeholder="Password", classes="span5")},
                                {"label": "How about: add a note to their account?", "content": ps.baseTextarea(name="adminNotes", classes="span5")},
                                {"label": "User level", "content": ps.baseSelect(elements=other, classes="span5", name="level")},
                                {"label": "Disable/Ban?", "content": ps.baseCheckbox(name="disable", label="Check to disable/ban the user")},
                                ps.baseHeading("Profile stuff...", size=3), "<hr>",
                                {"label": "Profile Visibility", "content": ps.baseCheckbox(name="visibility", label="Users public profile visibility. Checked for visibile")},
                                {"label": "About", "content": ps.baseTextarea(name="about", classes="span5")},
                                {"label": "Email", "content": ps.baseInput(type="email", name="email", placeholder="email@email.com", classes="span5")},
                                {"label": "Email Visibility", "content": ps.baseCheckbox(name="emailVisibility", label="Users email visibility. Checked for visibile")},
                                ]
                       )

                self.view.body = pageHead + editForm

        def POST(self):
                """

                """
                notes = self.members["adminNotes"]
                if not self.members.has_key("disable"): self.members["disable"] = False
                if not self.members.has_key("visibility"): self.members["visibility"] = False
                if not self.members.has_key("emailVisibility"): self.members["emailVisibility"] = False

                try:
                        user = profilem.profile()
                        user["adminNotes"] = notes
                        user["username"] = self.members["username"]

                        if self.members["password"]:
                                user["password"] = self.members["password"]

                        user["level"] = self.members["level"]
                        user["disable"] = self.members["disable"]
                        user["visibility"] = self.members["visibility"]
                        user["emailVisibility"] = self.members["emailVisibility"]
                        user["about"] = self.members["about"]
                        user["email"] = self.members["email"]

                        user.commit()

                        self.head = ("303 SEE OTHER", [("location", "/admin/users")])
                        c.session.pushAlert(("The user %s was created!" % ps.baseBold(user.username)), title="Congratulations!", icon="ok", type="success")

                except Exception as exc:
                        self.head = ("303 SEE OTHER", [("location", "/admin/users/new")])
                        c.session.pushAlert("Something went wrong while creating the user: %s. Heres the edit form again. Sorry!" % ps.baseBold(name), icon="fire", title="OH SNAP!", type="error")
