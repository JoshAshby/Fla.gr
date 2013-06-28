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
from seshat.route import autoRoute
from seshat.baseHTMLObject import baseHTMLObject

import models.couch.request.requestModel as rm
import models.couch.user.userModel as um


@autoRoute()
class index(baseHTMLObject):
    _title = "request an invite"
    _defaultTmpl = "public/request/request"
    def GET(self):
        """
        """
        if self.request.cfg.enableRequests:
            return self.view
        else:
            self._404()

    def POST(self):
        """
        """
        if self.request.cfg.enableRequests:
            email = self.request.getParam("email")

            found = um.userORM.find(email) or rm.requestORM.find(email)

            if email and not found:
                newRequest = rm.requestORM(email=email)
                newRequest.save()
                self.head = ("303 SEE OTHER",
                    [("location", "/request/thanks")])
                self.request.session.pushAlert("Thanks, %s for requesting an invite. \
                        We hope to get you a spot soon!"%email,
                        "", "success")
            else:
                if found:
                    self.request.session.pushAlert("There is already someone in our \
                            system with that email! If this is a mistake and \
                            you have not requested an invite or registered \
                            before, please send us an email.", "Wha'oh", "error")

                return self.view
        else:
            self._404()
