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

import flagr.models.flagModel as fm
import flagr.models.labelModel as lm
import models.profileModel as profilem

from flagr.objects.flagrObject import flagrObject as flagrPage
from seshat.route import route

import views.pyStrap.pyStrap as ps
import flagr.flagrConfig as fc

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
import os


@route("/search/flags")
class searchFlags_term(flagrPage):
        def GET(self):
                content = ""
                if not self.members.has_key("search"):
                        self.view["title"] = "Search flags"

                        pageHead = ps.baseColumn(ps.baseHeading("%s Search flags..."%ps.baseIcon("flag"), size=1) +
                                        ps.baseBasicForm(
                                                action=c.baseURL+"/search/flags",
                                                fields=[
                                                        ps.baseAppend(elements=[ps.baseInput(type="text", name="search", placeholder="Search", classes="span3 search-query"), ps.baseSubmit("Search", classes="btn-info")])
                                                        ],
                                                classes="form-search"),
                                        offset=3)

                        self.view.body = pageHead

                else:
                        term = self.members["search"]

                        ix = open_dir("index")
                        flags = []

                        with ix.searcher() as searcher:
                                query = MultifieldParser(["title", "description", "labels", "url", "author"], ix.schema).parse(unicode(term))
                                results = searcher.search(query)

                                for result in results:
                                        flags.append(fm.flag(result["id"]))

                        self.view["title"] = "Searching flags in: %s" % term

                        buildMessage = "Uh oh! Looks like I couldn't find any flags at the moment that fit that search criteria."

                        if flags:
                                flagList = fc.flagThumbnails(flags, 10)
                        else:
                                flagList = buildMessage

                        content = ps.baseRow(ps.baseColumn(flagList, id="flags"))

                        pageHead = ps.baseColumn(ps.baseHeading("%s Search flags..."%ps.baseIcon("flag"), size=1) +
                                        ps.baseBasicForm(
                                                action=c.baseURL+"/search/flags",
                                                fields=[
                                                        ps.baseAppend(elements=[ps.baseInput(type="text", name="search", placeholder="Search", value=term, classes="span3 search-query"), ps.baseSubmit("Search", classes="btn-info")])
                                                        ],
                                                classes="form-search"),
                                        offset=3)

                        self.view.body = pageHead + content
                        self.view.scripts = ps.baseScript("""
                                $('.btn-group').tooltip({
                                      selector: "a[rel=tooltip]"
                                })
                        """)
