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

flagSearchIndex = "/.flagSearchIndex"

storage = FileStorage(c.baseFolder+flagSearchIndex)


def flagSearch(queryString):
    """
    Searchs through the index for the given `queryString`

    :param queryString: The given query to search the index with
    :type queryString: Str
    :return: List of all found flags which have matches for QueryString
    :rtype: List
    """
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
