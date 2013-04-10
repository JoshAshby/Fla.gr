#!/usr/bin/env python
"""
fla.gr controller for registering after having an invite accepted
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.requests.requestsRegisterTmpl import requestsRegisterTmpl
import models.user.userModel as um
import models.request.requestModel as rm
import utils.signerUtils as su


@route("/request/register/(.*)")
class requestsRegister(baseHTMLObject):
    __name__ = "register"
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            token = self.env["members"][0]
            try:
                email = su.requestDetoken(token)
                view = requestsRegisterTmpl(searchList=[self.tmplSearchList])
                view.token = token
                view.email = email
                return view
            except:
                self.head = ("303 SEE OTHER", [("Location", "/request")])
                self.session.pushAlert("We couldn't find that invite in our \
                        system, are you sure it's correct?", "Oh no!", "error")
        else:
            self.head = ("404 NOT FOUND", [])

    def POST(self):
        """
        """
        if self.env["cfg"].enableRequests:
            token = self.env["members"][0]
            givenEmail = self.env["members"]["email"] \
                    if self.env["members"].has_key("email") else ""
            username = self.env["members"]["username"] \
                    if self.env["members"].has_key("username") else ""
            passwordOnce  = self.env["members"]["passwordOnce"] \
                    if self.env["members"].has_key("passwordOnce") else ""
            passwordTwice  = self.env["members"]["passwordTwice"] \
                    if self.env["members"].has_key("passwordTwice") else ""

            email = su.requestDetoken(token)
            foundEmail = um.findByEmail(email)
            foundName = um.findByUsername(username)

            if email == givenEmail \
                    and passwordOnce == passwordTwice \
                    and passwordOnce != "" \
                    and not (foundEmail or foundName):
                #Passwords match, emails match, password isn't null and no one
                #Else has the same username or email. If this is all true then
                #We can go ahead and make a new user and while we're at it
                #lets log them in also. When this happends we delete the request
                #also so its not just sitting around in our system
                newUser = um.userORM(username, passwordOnce)
                newUser.loginThis(self.env["cookie"])
                newUser.save()
                req = rm.requestORM.find(email)
                req.delete()
                self.session.pushAlert("You can now log in with the \
                        information you gave us!", "Congrats!", "success")
                self.head = ("303 SEE OTHER", [("location", "/your/flags")])

            else:
                #If none, or one of those isn't true then we have a problem...
                view = requestsRegisterTmpl(searchList=[self.tmplSearchList])
                view.email = givenEmail
                view.token = token
                view.username = username
                if foundName:
                    #Someone with the same username, thats not allowed...
                    self.session.pushAlert("There is already a person in our \
                            system with that username, please choose another",
                            "Oh no!", "error")

                    view.usernameError = True

                elif foundEmail:
                    #Already someone with that email in the system...
                    self.session.pushAlert("There is already someone with that \
                            email in our system, are you sure you don't already\
                            have an account, or have already requested an invite?",
                            "Oh no!", "error")
                    view.emailError = True

                elif passwordOnce != "" and passwordOnce != passwordTwice:
                    #Password isn't null but doesn't match
                    view.passwordMatchError = True

                elif email != givenEmail:
                    #And finally, if the email they give doesn't match the invites
                    #email...
                    view.emailMatchError = True

            return view

        else:
            self.head = ("404 NOT FOUND", [])
