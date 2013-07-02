#!/usr/bin/env python
"""
fla.gr controller for editing a request
Currently this only will grant a request

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseObject import HTMLObject
from seshat.objectMods import *

import models.couch.request.requestModel as rm
import models.redis.setting.settingModel as sm
import utils.email.emailUtils as eu


# Fuck this page in general
#@autoRoute()
#@admin()
#class grant(HTMLObject):
    #def POST(self):
        #if self.request.cfg.enableRequests:
            #id = self.request.id
                #req = rm.requestORM.find(ID)
                #regToken = req.generateToken()
                #tmplData[req.email] = {"email": req.email,
                        #"registerToken": regToken}
                #emails.append(req.email)

            #try:
                #eu.sendMessage(tmplID, tmplData, emails, "fla.gr Invite")
                #self.session.pushAlert("You granted the requests! A special \
                        #email is on the way to them, as a result of your kind \
                        #actions", ":)", "success")
            #except Exception as exc:
                #self.session.pushAlert("OH NO! One or all of the grant \
                        #messages didn't send. Heres the error: %s"%exc,
                        #"FAILURE!" "error")

            #self.head = ("303 SEE OTHER", [("location", "/admin/requests")])
        #else:
            #self._404()
