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

import flagr.models.flagModel as fm
import flagr.models.labelModel as lm
from flagr.objects.flagrObject import flagrObject
import flagr.views.pyStrap.pyStrap as ps
import flagr.config.flagrConfig as fc


@route("/labels")
class labelIndex(flagrObject):
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
                        ps.baseColumn(ps.baseHeading("%s Public Labels" % (ps.baseIcon("tags")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                if not labelList:
                        labelList = "Oh no! There are not any public labels currently available!"

                self.view.body = ps.baseRow(pageHead)+labelList


@route("/flags")
class labelPublic(flagrObject):
        def GET(self):
                start = int(self.members["start"]) if self.members.has_key("start") else 0

                flags = fm.flagList(md=True)

                nextClass = ""
                prevClass = ""

                if start == 0:
                        prevClass = "disabled"
                        prevLink = "#"
                elif start == 10:
                        prevLink = c.baseURL+"/flags"
                else:
                        prevLink = c.baseURL+"/flags?start=" + str(start-10)

                if len(flags[start+10:start+20]) <= 0:
                        nextClass = "disabled"
                        nextLink = "#"
                else:
                        nextLink = c.baseURL+"/flags?start=" + str(start+10)

                flags = flags[start:start+10]

                pager = """<ul class="pager">
        <li class="previous %s">
                <a href="%s">&larr; Previous</a>
        </li>
        <li class="next %s">
                <a href="%s">Next &rarr;</a>
        </li>
</ul>""" % (prevClass, prevLink, nextClass, nextLink)

                if self.members.has_key("view"): view = self.members["view"]
                else: view = ""

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
                        ps.baseColumn(ps.baseHeading("%s Public Flags" % (ps.baseIcon("flag")), size=2), width=5),
                        ps.baseColumn(ps.baseUL(tabs, classes="nav nav-tabs"), width=5)
                        ])

                buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags just yet!"

                if flags:
                        flagList = fc.flagThumbnails(flags)
                else:
                        flagList = buildMessage

                self.view.body = pageHead + ps.baseRow(ps.baseColumn(flagList, id="flags")) + pager



