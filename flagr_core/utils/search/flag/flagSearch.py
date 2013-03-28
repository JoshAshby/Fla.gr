#!/usr/bin/env python
"""
Various helpers for querying the flag search index
"""
import config.config as c

from whoosh.filedb.filestore import FileStorage
from whoosh.qparser import MultifieldParser

import logging
logger = logging.getLogger(c.logName+".searchUtils.flagSearch")

import models.flag.flagModel as fm
import config.dbBase as db

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
            flags.append(fm.flagORM.load(db.couchServer, result["id"]))

    flags = fm.formatFlags(flags, False)

    return flags
