#!/usr/bin/env python2
"""
Fla.gr - Personal Memory

You controller. Everything under the /you
        URL is handled and fleshed out, or linked to
        from here.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from seshat.route import route

from flagr.objects.flagrObject import flagrObject
import flagr.views.pyStrap.pyStrap as ps
import flagr.config.flagrConfig as fc

import logging
logger = logging.getLogger(c.logName+".search")


@route("/search/flags")
class searchFlags_term(flagrObject):
    def GET(self):
        self.view["title"] = "Search flags"

        value = self.members["search"] if self.members.has_key("search") else ""

        pageHead = ps.baseHeading("%s Search flags..."%ps.baseIcon("search"),
                size=2)
        pageHead += ps.baseBasicForm(
            action=c.baseURL+"/search/flags",
            fields=[
                ps.baseAppend(elements=[
                    ps.baseInput(type="text",
                        name="search",
                        placeholder="Search",
                        classes="span3",
                        value=value),
                    ps.baseButton(ps.baseIcon("search"),
                        type="submit",
                        classes="btn")
                    ])
                ],
            classes="form-inline")

        pageHead = ps.baseColumn(pageHead, offset=3)

        self.view.body = pageHead

        content = fc.flagSearch(members=self.members)
        if content:
            self.view.body += content
            self.view["title"] = "Searching flags in: %s" % value
