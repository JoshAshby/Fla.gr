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

from flagr.objects.publicObject import publicObject
import flagr.views.pyStrap.pyStrap as ps

import models.profileModel as profilem


@route("/login")
@route("/auth/login")
class login(publicObject):
    __menu__ = "Login"
    def GET(self):
        """
        Display the login page.
        """
        if c.session.loggedIn:
            self.head = ("303 SEE OTHER",
                [("location", "/your/flags")])
            c.session.pushAlert("Hey look, you're already signed in!")

        else:
            loginForm = ps.baseHeading("Please Login...", size=2)
            loginForm += ps.baseHorizontalForm(action=c.baseURL+"/auth/login",
                method="POST",
                fields=[
                {"content": ps.baseInput(type="text",
                    name="username",
                    placeholder="Username", classes="span6")},
                "<br><br>",
                {"content": ps.baseInput(type="password",
                    name="password",
                    placeholder="Password",
                    classes="span6")}],
                actions = [ps.baseSubmit("Login"), " or ",
                    ps.baseAnchor("Register",
                        link=c.baseURL+"/auth/register")])

            self.view["body"] = ps.baseColumn(loginForm,
                width=6,
                offset=2)

    def POST(self):
        """
        Use form data to check login, and the redirect if successful
        if not redirect to login page again.
        """
        passwd = self.members["password"]
        name = self.members["username"]

        try:
            c.session.login(name, passwd)
            self.head = ("303 SEE OTHER", [("location", "/your/flags")])
            c.session.pushAlert("Welcome back, %s!" % name)

        except Exception as exc:
            self.head = ("303 SEE OTHER", [("location", "/auth/login")])
            c.session.pushAlert("Something went wrong:<br>%s Please try again." % exc,
                type="error",
                title="Oh no!",
                icon="fire")


@route("/logout")
@route("/auth/logout")
class logout(publicObject):
    def GET(self):
        """
        Simply log the user out. Nothing much to do here.

        redirect to login page after we're done.
        """
        c.session.logout()

        self.head = ("303 SEE OTHER", [("location", ("/auth/login"))])


@route("/register")
@route("/auth/register")
class register(publicObject):
    def GET(self):
        """
        """
        self.view["title"] = "Register for an account"
        pageHead = ps.baseHeading("%s Register an account %s" % (
                ps.baseIcon("group"),
                ps.baseSmall("Only four simple steps!")
            ),
            size=1)

        pageHead += ps.baseParagraph("Please note all fields are required and your account will not be active until we send you an email saying it is. You are registering for a closed alpha account.")

        editForm = ps.baseHorizontalForm(action=(c.baseURL+"/auth/register"),
            method="POST",
            actions=[ps.baseSubmit("%s 4) Register! (Thats it!)"%ps.baseIcon("save"),
                classes="btn-info")],
            fields=[
                ps.baseHeading("1) Choose a username... %s" % ps.baseSmall(
                        "Something funny or lame, we don't care!"),
                    size=3),
                {"content": ps.baseInput(type="text",
                    placeholder="Username",
                    name="username",
                    classes="span10")},
                ps.baseHeading("2) Setup your password... %s"%ps.baseSmall(
                        "Both fields please"),
                    size=3),
                {"content": ps.baseInput(type="password",
                    name="newpassword",
                    placeholder="Password",
                    classes="span10")},
                "<br><br>",
                {"content": ps.baseInput(type="password",
                    name="newtwopassword",
                    placeholder="Repeat password",
                    classes="span10")},
                ps.baseHeading("3) Setup an email %s" % ps.baseSmall(
                        "Just for us to contact you with when your account is ready to go..."),
                    size=3),
                {"content": ps.baseInput(type="email",
                    name="email",
                    placeholder="email@email.com",
                    classes="span10"),
                    "help": ps.baseSmall("For a beta account you do have to register an email so we can contact you about your account.")},
                ]
           )

        self.view["body"] = pageHead + editForm

def POST(self):
        """
        """
        if not self.members["username"] or not self.members["newpassword"] or not self.members["newtwopassword"] or not self.members["email"]:
            self.head = ("303 SEE OTHER", [("location", "/auth/register")])
            c.session.pushAlert("You need to fill out the username, email and both password fields!",
                icon="fire",
                title="OH SNAP!",
                type="error")

        try:
            test = profilem.findUser(self.members["username"])
            if test:
                self.head = ("303 SEE OTHER", [("location", "/auth/register")])
                c.session.pushAlert("The username %s is already taken. Pick a new one and try again!" % ps.baseBold(self.members["username"]),
                    icon="fire",
                    title="OH SNAP!",
                    type="error")
            else:
                user = profilem.profile()
                user["email"] = self.members["email"]
                user["username"] = self.members["username"]

                if self.members["newpassword"] == self.members["newtwopassword"]:
                    user["password"] = self.members["newpassword"]
                    user["disable"] = True

                    user.commit()

                    self.head = ("303 SEE OTHER", [("location", "/auth/thanks")])
                    c.session.pushAlert(("You've been registered! Hold tight and we'll send you an email when you're account is active!"),
                        title="Congratulations!",
                        icon="ok",
                        type="success")

                else:
                    raise Exception("Passwords need to match!")

        except Exception as exc:
            self.head = ("303 SEE OTHER", [("location", "/auth/register")])
            c.session.pushAlert("Something went wrong while registering, heres the deal:%s" % exc,
                icon="fire",
                title="OH SNAP!",
                type="error")


@route("/auth/thanks")
class authThanks(publicObject):
    def GET(self):
            pass
