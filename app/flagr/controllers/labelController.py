#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

label controller. Everything under the /labels
        URL is fleshed out, or linked to from here.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

import flagr.models.flagModel as fm
import flagr.models.labelModel as lm

from flagr.objects.flagrObject import flagrObject as flagrPage
from seshat.route import route

import views.pyStrap.pyStrap as ps
import flagr.flagrConfig as fc


@route("/labels")
class labelIndex(flagrPage):
        def GET(self):
                labelList = lm.labelList()

                self.view["title"] = "Public Labels"

                tabs = "<li>" + ps.baseAnchor(ps.baseIcon("flag"), link="/flags",
                                rel="tooltip",
                                data=[("original-title", "Public Flags"),
                                        ("placement", "bottom")]) + "</li>"
                tabs += "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("tags"), link="/labels",
                                rel="tooltip",
                                data=[("original-title", "Public Labels"),
                                        ("placement", "bottom")]) + "</li>"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Public Labels" % (ps.baseIcon("tags")), size=1), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                if not labelList:
                        labelList = "Oh no! There are not any public labels currently available!"

                self.view.body = ps.baseRow(pageHead)+labelList


@route("/flags")
class labelPublic(flagrPage):
        def GET(self):
                if self.members.has_key("view"): view = self.members["view"]
                else: view = ""

                flags = fm.flagList(md=True)
                self.view["title"] = "Public Flags"

                tabs = "<li class=\"active\">" + ps.baseAnchor(ps.baseIcon("flag"), link="/flags",
                                rel="tooltip",
                                data=[("original-title", "Public Flags"),
                                        ("placement", "bottom")]) + "</li>"
                tabs += "<li>" + ps.baseAnchor(ps.baseIcon("tags"), link="/labels",
                                rel="tooltip",
                                data=[("original-title", "Public Labels"),
                                        ("placement", "bottom")]) + "</li>"

                pageHead = ps.baseRow([
                        ps.baseColumn(ps.baseHeading("%s Public Flags" % (ps.baseIcon("flag")), size=1), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags just yet!"

                if flags:
                        width=10

                        flagList = fc.flagThumbnails(flags, width)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow(ps.baseColumn(flagList, id="flags"))


@route("/label/(.*)")
class labelView(flagrPage):
        def GET(self):
                label = self.members[0]
                flags = lm.labeledFlagList(label, md=True)
                view = self.members["view"] if self.members.has_key("view") else ""

                self.view["title"] = "Flags in label: %s" % label

                labels = label.split("/")
                labs = [ps.baseAnchor(labels[0], link=c.baseURL+"/label/%s" % labels[0])]

                for lab in range(1, len(labels)):
                        link = labs[lab-1]["link"]+"/%s" % labels[lab]
                        labs.append(ps.baseAnchor(labels[lab], link=link))

                stack = ""

                for lab in labs:
                        stack += lab + "/"

                stack = stack.strip("/")

                pageHead = ps.baseColumn(ps.baseHeading("%s Flags in label: %s" % (ps.baseIcon("tag"), stack), size=1))

                pageHead = ps.baseRow(pageHead)

                labelsUnder = lm.labelsUnderList(label)

                if not labelsUnder:
                        labelsUnder = "You've hit bottom! There's nothing stacked under this label!"

                pageHead += ps.baseRow([ps.baseColumn(ps.baseBold("%s Stacked labels:"%ps.baseIcon("tags"), classes="muted")), ps.baseColumn(labelsUnder)])


                buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags under this label just yet!"

                if flags:
                        width=10

                        flagList = fc.flagThumbnails(flags, width)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow(ps.baseColumn(flagList, id="flags"))
