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
    for flag in flagsList:
        if not flag.visibility and not showAll:
            flagsList.pop(flagsList.index(flag))
        else:
            flag.formatedDescription = mdu.markClean(flag.description)
            flag.formatedDate = datetime.strftime(flag.created, "%a %b %d, %Y @ %H:%I%p")

    return flagsList


def formatFlag(flag):
    flag.formatedDescription = mdu.markClean(flag.description)
    flag.formatedDate = datetime.strftime(flag.created, "%a %b %d, %Y @ %H:%I%p")
    return flag


class flagORM(Document):
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

    def save(self):
        self.store(db.couchServer)
