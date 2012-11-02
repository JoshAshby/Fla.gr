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

from seshat.route import route

import flagr.models.labelModel as lm
from flagr.objects.flagrObject import flagrObject
import flagr.views.pyStrap.pyStrap as ps
import flagr.config.flagrConfig as fc


@route("/label/(.*)")
class labelView(flagrObject):
        def GET(self):
                label = self.members[0]
                flags = lm.labeledFlagList(label, md=True)

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

                pageHead = ps.baseColumn(ps.baseHeading("%s Flags in label: %s" % (ps.baseIcon("tag"), stack), size=2))

                pageHead = ps.baseRow(pageHead)

                labelsUnder = lm.labelsUnderList(label)

                if not labelsUnder:
                        labelsUnder = "You've hit bottom! There's nothing stacked under this label!"

                pageHead += ps.baseRow([ps.baseColumn(ps.baseBold("%s Stacked labels:"%ps.baseIcon("tags"), classes="muted")), ps.baseColumn(labelsUnder)]) + "<br />"


                buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags under this label just yet!"

                if flags:
                        flagList = fc.flagThumbnails(flags)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow(ps.baseColumn(flagList, id="flags"))
