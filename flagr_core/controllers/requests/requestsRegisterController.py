#!/usr/bin/env python
"""
fla.gr controller for registering after having an invite accepted

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.requests.requestsRegisterTmpl import requestsRegisterTmpl
import models.user.userModel as um
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
                self.session.pushAlert("We couldn't find that invite in our system, are you sure it's correct?", "Oh no!", "error")
        else:
            self.head = ("404 NOT FOUND", [])

    def POST(self):
        """
        """
        if self.env["cfg"].enableRequests:
            token = self.env["members"][0]
            givenEmail = self.env["members"]["email"] if self.env["members"].has_key("email") else ""
            username = self.env["members"]["username"] if self.env["members"].has_key("username") else ""
            passwordOnce  = self.env["members"]["passwordOnce"] if self.env["members"].has_key("passwordOnce") else ""
            passwordTwice  = self.env["members"]["passwordTwice"] if self.env["members"].has_key("passwordTwice") else ""
            email = su.requestDetoken(token)
            if email == givenEmail and passwordOnce == passwordTwice and passwordOnce != "":
                newUser = um.userORM.new(username, passwordOnce)
                newUser.loginThis(self.env["cookie"])
                newUser.save()
                self.session.pushAlert("You can now log in with the information you gave us!", "Congrats!", "success")
                self.head = ("303 SEE OTHER", [("location", "/auth/login")])
            elif passwordOnce != "" and passwordOnce != passwordTwice:
                view = requestsRegisterTmpl(searchList=[self.tmplSearchList])
                view.passwordMatchError = True
                view.email = givenEmail
                view.token = token
                view.username = username
                return view
            elif email != givenEmail:
                view = requestsRegisterTmpl(searchList=[self.tmplSearchList])
                view.emailMatchError = True
                view.email = givenEmail
                view.token = token
                return view
        else:
            self.head = ("404 NOT FOUND", [])
