#!/usr/bin/env python
"""
fla.gr flag model

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from couchdb.mapping import Document, TextField, DateTimeField, BooleanField, ListField
from datetime import datetime

import config.dbBase as db
from models.couch.baseCouchModel import baseCouchModel
import models.couch.user.userModel as um
import utils.markdownUtils as mdu


def listFlagsByUserID(userID):
    """
    Searches couchdb for flags by the requested userID

    :param userID: The userID to search for
    :return: A list of `flagORM` instances at least one flag is found, and the
        `userORM` object for the flags author
        `None` if no flags are found
    """
    foundFlags = flagORM.view(db.couchServer, 'typeViews/flag')
    if not foundFlags:
        return None
    flags = []
    for flag in foundFlags:
        if flag.userID == userID:
            flags.append(flag)
    return flags

def formatFlags(flagsList, showAll):
    """
    Takes a list of `flagORM`s and formates the datetime and markdown
    for templates. Also can remove non public flags, if `showAll` is `False`

    :params flagsList: A list object of `flagORMs` to format
    :params showAll: If `False` Then private flags will be removed from the list
    :return: A list of formated `flagORM` objects
    """
    flags = []
    for flag in flagsList:
        if showAll:
            flags.append(formatFlag(flag))
        else:
            if flag.visibility:
                flags.append(formatFlag(flag))

    return flags


def formatFlag(flag):
    """
    Same as above, however takes a single `flagORM` and formates the datetime
    markdown.

    :param flag: The `flagORM` object of the flag to format
    :return:
    """
    flag.formatedDescription = mdu.markClean(flag.description)
    flag.formatedDate = datetime.strftime(flag.created, "%a %b %d, %Y @ %H:%I%p")
    flag.author = um.userORM.find(flag.userID)
    return flag


class flagORM(Document, baseCouchModel):
    _view = "typeViews/flag"
    userID = TextField()
    title = TextField()
    description = TextField()
    url = TextField()
    labels = ListField(TextField())
    visibility = BooleanField(default=False)
    created = DateTimeField(default=datetime.now)
    docType=TextField(default="flag")
    formatedDescription = ""
    formatedDate = ""
    author = ""
