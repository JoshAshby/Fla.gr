#!/usr/bin/env python
"""
Various helpers for querying the flag search index

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import config.config as c

from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import MultifieldParser

import logging
logger = logging.getLogger(c.logName+".searchUtils.flagSearch")

import models.couch.flag.flagModel as fm

flagSearchIndex = "/.flagSearchIndex"

storage = FileStorage(c.baseFolder+flagSearchIndex)


def flagSearch(queryString):
    flags = []
    ix = storage.open_index()

    with ix.searcher() as searcher:
        query = MultifieldParser(
            ["title",
            "description",
            "labels",
            "url"], ix.schema).parse(unicode(queryString))
        results = searcher.search(query)

        for result in results:
            flags.append(fm.flagORM.getByID(result["id"]))

    flags = fm.formatFlags(flags, False)

    return flags
