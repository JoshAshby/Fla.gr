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


def listFlagsByUserID(userID):
    """
    Searches couchdb for flags by the requested userID

    :param userID: The userID to search for
    :return: A list of `flagORM` instances at least one flag is found,
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


class flagORM(Document):
    userID = TextField()
    flag = TextField()
    url = TextField()
    tags = ListField()
    public = BooleanField(default=False)
    made = DateTimeField(default=datetime.now)
    docType=TextField(default="flag")

    def save(self):
        self.store(db.couchServer)
