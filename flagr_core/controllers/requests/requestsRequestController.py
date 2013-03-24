#!/usr/bin/env python
"""
fla.gr controller for requesting an invite

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.requests.requestsRequestTmpl import requestsRequestTmpl

import models.request.requestModel as rm
import models.user.userModel as um


@route("/request")
class requestsRequests(baseHTMLObject):
    __name__ = "request an invite"
    def GET(self):
        """
        """
        if self.env["cfg"].enableRequests:
            view = requestsRequestTmpl(searchList=[self.tmplSearchList])
            return view
        else:
            self.head = ("404 NOT FOUND", [])

    def POST(self):
        """
        """
        if self.env["cfg"].enableRequests:
            email = self.env["members"]["email"] \
                    if self.env["members"].has_key("email") else ""

            found = um.userORM.find(email) or rm.requestORM.find(email)

            if email and not found:
                newRequest = rm.requestORM.new(email)
                newRequest.save()
                self.head = ("303 SEE OTHER",
                    [("location", "/request/thanks")])
                self.session.pushAlert("Thanks, %s for registering. \
                        We hope to get you an invite soon!"%email,
                        "", "success")
            else:
                if found:
                    self.session.pushAlert("There is already someone in our \
                            system with that email! If this is a mistake and \
                            you have not requested an invite or registered \
                            before, please send us an email \
                            at: flagr@joshashby.com", "Wha'oh", "error")

                view = requestsRequestTmpl(searchList=[self.tmplSearchList])
                view.emailError = True
                return view
        else:
            self.head = ("404 NOT FOUND", [])
