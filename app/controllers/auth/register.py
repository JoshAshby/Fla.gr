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
                newUser.loginThis(self.env["cookie"])
                newUser.save()
                self.session.pushAlert("You can now log in with the \
                        information you gave us!", "Congrats!", "success")
                self.head = ("303 SEE OTHER", [("location", "/your/flags")])

            #else:
                #"""
                #If none, or one of those isn't true then we have a problem...
                #"""
                #view.email = givenEmail
                #view.username = username
                #if foundName:
                    #"""
                    #Someone with the same username, thats not allowed...
                    #"""
                    #self.session.pushAlert("There is already a person in our \
                            #system with that username, please choose another",
                            #"Oh no!", "error")

                    #view.usernameError = True

                #elif foundEmail:
                    #"""
                    #Already someone with that email in the system...
                    #"""
                    #self.session.pushAlert("There is already someone with that \
                            #email in our system, are you sure you don't already\
                            #have an account, or have already requested an invite?",
                            #"Oh no!", "error")
                    #view.emailError = True

                #elif passwordOnce != "" and passwordOnce != passwordTwice:
                    #"""
                    #Password isn't null but doesn't match
                    #"""
                    #view.passwordMatchError = True

            #return self.view

        else:
            self._404()
