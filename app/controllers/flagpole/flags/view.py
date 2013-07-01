#!/usr/bin/env python
"""
fla.gr controller for viewing and editing individual flags

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

from models.couch.flag.flagModel import flagORM
from models.couch.user.userModel import userORM
import models.couch.flag.collections.userPublicFlagsCollection as pubfc

import json


@autoRoute()
@admin()
class view(HTMLObject):
    _title = "flagpole flag"
    _defaultTmpl = "flagpole/flags/singleFlag"
    def GET(self):
        """
        """
        flagid = self.request.id

        flag = flagORM.getByID(flagid)
        user = userORM.getByID(flag.userID)

        scripts = []

        if self.request.cfg.enableDynamicLabels:
            scripts.extend(["handlebars_1.0.min",
                    "jquery.json-2.4.min",
                    "dynamicInput.flagr"])
            labels = json.dumps(flag.labels)
        else:
            labels = flag.labels.join(", ")

        self.view.data = {"flag": flag,
            "labels": labels,
            "user": user}

        self.view.scripts = scripts

        return self.view

    def POST(self):
        flagid = self.request.id
        title = self.request.getParam("title")
        description = self.request.getParam("description")
        labels = self.request.getParam("labels")
        url = self.request.getParam("url")
        visibility = self.request.getParam("visibility")

        try:
            labels = list(set(json.loads(labels)))
        except:
            labels = list(set(labels.strip(" ").split(",")))

        flag = flagORM.getByID(flagid)
        flag.title = title
        flag.description = description
        flag.labels = labels
        flag.url = url

        if flag.visibility != visibility:
            pubFlags = pubfc.userPublicFlagsCollection(flag.userID)
            if visibility:
                pubFlags.addObject(flag.id)
            else:
                pubFlags.delObject(flag.id)

            flag.visibility = visibility

        flag.save()


        self.request.session.pushAlert("Flag `%s` updated" % flag.title, "Yay", "success")

        self.head = ("303 SEE OTHER",
            [("location", "/flagpole/flags/view/"+str(flag.id))])
