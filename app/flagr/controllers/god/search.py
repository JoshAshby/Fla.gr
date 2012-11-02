#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
controller for authentication stuff.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

from flagr.objects.godObject import godObject
from seshat.route import route
import flagr.views.pyStrap.pyStrap as ps
import flagr.config.flagrConfig as fc
import flagr.models.flagModel as fm

import logging
logger = logging.getLogger(c.logName+".deitySearch")

from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
import os

path = os.path.dirname(c.__file__)


@route("/god/search")
class searchIndex_god(godObject):
        __menu__ = "Deity Search"
        def GET(self):
                content = ""
                self.view["title"] = "Deity Search flags"

                value = self.members["search"] if self.members.has_key("search") else ""

                pageHead = ps.baseColumn(ps.baseHeading("%s Search flags..."%ps.baseIcon("search"), size=2) +
                                ps.baseBasicForm(
                                        action=c.baseURL+"/god/search",
                                        fields=[
                                                ps.baseAppend(elements=[ps.baseInput(type="text", name="search", placeholder="Search", classes="span3", value=value), ps.baseButton(ps.baseIcon("search"), type="submit", classes="btn")])
                                                ],
                                        classes="form-inline"),
                                offset=2)

                if not self.members.has_key("search"):
                        self.view.body = pageHead

                else:
                        term = self.members["search"]

                        ix = open_dir(path+"/.searchIndex")
                        flags = []

                        with ix.searcher() as searcher:
                                query = MultifieldParser(["title", "description", "labels", "url", "author"], ix.schema).parse(unicode(term))
                                results = searcher.search(query)

                                for result in results:
                                        flags.append(fm.flag(result["id"]))

                        self.view["title"] = "Searching flags in: %s" % term

                        buildMessage = "Uh oh! Looks like I couldn't find any flags at the moment that fit that search criteria."

                        start = int(self.members["start"]) if self.members.has_key("start") else 0

                        nextClass = ""
                        prevClass = ""

                        if start == 0:
                                prevClass = "disabled"
                                prevLink = "#"
                        elif start == 10:
                                prevLink = c.baseURL+"/god/search"
                        else:
                                prevLink = c.baseURL+"/god/search?start=" + str(start-10)

                        if len(flags[start+10:start+20]) <= 0:
                                nextClass = "disabled"
                                nextLink = "#"
                        else:
                                nextLink = c.baseURL+"/god/search?start=" + str(start+10)

                        flags = flags[start:start+10]

                        pager = """<ul class="pager">
                <li class="previous %s">
                        <a href="%s">&larr; Previous</a>
                </li>
                <li class="next %s">
                        <a href="%s">Next &rarr;</a>
                </li>
        </ul>""" % (prevClass, prevLink, nextClass, nextLink)


                        if flags:
                                flagList = fc.deityFlagThumbnails(flags)
                        else:
                                flagList = buildMessage

                        content = ps.baseRow(ps.baseColumn(flagList, id="flags"))

                        self.view.body = pageHead + content + pager


@route("/god/search/reindex")
class searchIndex_god(godObject):
        __menu__ = "Deity Search Index Rebuild"
        def GET(self):
                pass
        def POST(self):
                pass
