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
                pageHead = ps.baseColumn(ps.baseHeading("%s Public labels" % (ps.baseIcon("globe")), size=1))

                if not labelList:
                        labelList = "Oh no! There are not any public labels currently available!"

                self.view.body = ps.baseRow(pageHead)+"<hr>"+labelList


@route("/flags")
@route("/public")
@route("/label/public")
@route("/label/public/view")
@route("/labels/view/public")
class labelPublic(flagrPage):
        def GET(self):
                if self.members.has_key("view"): view = self.members["view"]
                else: view = ""

                flags = fm.flagList(md=True)
                self.view["title"] = "Public Flags"
                pageHead = ps.baseColumn(ps.baseHeading("%s Public flags" % (ps.baseIcon("globe")), size=1))

                pageHead = ps.baseRow(pageHead)+"<hr>"

                buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags just yet!"

                if flags:
                        width=10

                        flagList = fc.flagThumbnails(flags, width)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow(ps.baseColumn(flagList, id="flags"))
                self.view.scripts = ps.baseScript("""
                $('.btn-group').tooltip({
                      selector: "a[rel=tooltip]"
                })
""")


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

                other = ""
                if c.session.loggedIn:
                        toggle = ps.baseAButton(ps.baseIcon("user"), classes="",
                                                link="#",
                                                id="viewYou",
                                                data=[("original-title", "Toggle your flags")],
                                                rel="tooltip")

                pageHead = ps.baseRow(pageHead)+"<hr>"

                labelsUnder = lm.labelsUnderList(label)

                if not labelsUnder:
                        labelsUnder = "You've hit bottom! There's nothing stacked under this label!"

                pageHead += ps.baseRow([ps.baseColumn(ps.baseBold("%s Stacked labels:"%ps.baseIcon("tags"), classes="muted")), ps.baseColumn(labelsUnder)])+"<hr>"


                buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags under this label just yet!"

                if flags:
                        width=10

                        flagList = fc.flagThumbnails(flags, width)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow(ps.baseColumn(flagList, id="flags"))
                self.view.scripts = ps.baseScript("""
                $('.btn-group').tooltip({
                      selector: "a[rel=tooltip]"
                })

                $("#viewYou").click(function() {
                        $(".you").toggle()
                        })
""")
