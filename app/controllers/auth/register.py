#!/usr/bin/env python
"""
fla.gr controller for registering 

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseHTMLObject import baseHTMLObject

import models.couch.user.userModel as um


@autoRoute()
class register(baseHTMLObject):
    _title = "register"
    def GET(self):
        """
        """
        if self.request.cfg.enableRegistration:
            return self.view
        else:
            self.head = ("303 SEE OTHER", [("Location", "/request")])
            self.request.session.pushAlert("We currently have registration closed \
                    however you can request an invite on this page",
                    "Oh no!", "error")

    def POST(self):
        """
        """
        if self.request.cfg.enableRegistration:
            givenEmail = self.request.getParam("email")
            username = self.request.getParam("username")
            passwordOnce = self.request.getParam("passwordOnce")
            passwordTwice = self.request.getParam("passwordTwice")

            foundEmail = um.findByEmail(givenEmail)
            foundName = um.findByUsername(username)

            if passwordOnce == passwordTwice \
                    and passwordOnce != "" \
                    and not (foundEmail or foundName):
                """
                Passwords match, password isn't null and no one
                Else has the same username or email. If this is all true then
                We can go ahead and make a new user and while we're at it
                lets log them in also.
                """
                newUser = um.userORM(username, passwordOnce)
                newUser.save()
                self.request.session.loginWithoutCheck(username)
                self.request.session.pushAlert("You're account has been made and we've logged you in!",
                    "Congrats!", "success")
                self.head = ("303 SEE OTHER", [("location", "/your/flags")])
                return

            else:
                """
                If none, or one of those isn't true then we have a problem...
                """
                if foundName:
                    """
                    Someone with the same username, thats not allowed...
                    """
                    self.request.session.pushAlert("There is already a person in our \
                            system with that username, please choose another",
                            "Oh no!", "error")

                    self.view.data = {"usernameError": True}

                elif foundEmail:
                    """
                    Already someone with that email in the system...
                    """
                    self.request.session.pushAlert("There is already someone with that \
                            email in our system, are you sure you don't already\
                            have an account, or have already requested an invite?",
                            "Oh no!", "error")

                    self.view.data = {"emailError": True,
                        "username": username}

                elif passwordOnce != "" and passwordOnce != passwordTwice:
                    """
                    Password isn't null but doesn't match
                    """
                    self.request.session.pushAlert("Your passwords don't match!", "Oh no!", "error")
                    self.view.data = {"passwordError": True,
                        "username": username,
                        "email": givenEmail}

                return self.view

        else:
            self._404()
