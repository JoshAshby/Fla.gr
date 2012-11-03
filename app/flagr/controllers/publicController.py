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

        tabs = fc.tabs([
            {"title": "Public Flags",
                "link": c.baseURL+"/flags",
                "icon": "flag"},
            {"active": True,
                "title": "Public Labels",
                "link": c.baseURL+"/labels",
                "icon": "tags"},
            ])

        pageHead = ps.baseRow([
            ps.baseColumn(
                ps.baseHeading("%s Public Labels" % (ps.baseIcon("tags")),
                    size=2),
            width=5),
            ps.baseColumn(tabs,
                width=5)
            ])

        if not labelList:
            labelList = "Oh no! There are not any public labels currently available!"

        self.view.body = ps.baseRow(pageHead)+labelList


@route("/flags")
class labelPublic(flagrObject):
    def GET(self):
        flags = fm.flagList(md=True)

        flags, pager = fc.listPager(flags,
            "/flags",
            self.members)

        self.view["title"] = "Public Flags"

        tabs = fc.tabs([
            {"active": True,
                "title": "Public Flags",
                "link": c.baseURL+"/flags",
                "icon": "flag"},
            {"title": "Public Labels",
                "link": c.baseURL+"/labels",
                "icon": "tags"},
            ])

        pageHead = ps.baseRow([
            ps.baseColumn(
                ps.baseHeading("%s Public Flags" % (ps.baseIcon("flag")),
                    size=2),
            width=5),
            ps.baseColumn(tabs,
                width=5)
        ])

        buildMessage = "OH NO! Either something went wrong, or there aren't any publicly visible flags just yet!"

        if flags:
            flagList = fc.flagThumbnails(flags)
        else:
            flagList = buildMessage

        self.view.body = pageHead
        self.view.body += ps.baseRow(
            ps.baseColumn(flagList, id="flags")
        )
        self.view.body += pager
