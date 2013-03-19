#!/usr/bin/env python
"""
fla.gr request model for invite requests

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from couchdb.mapping import Document, TextField, DateTimeField
from datetime import datetime

import config.dbBase as db


def formatRequests(requestsList):
    """
    Takes a list of `requestORM`s and formates the datetime

    :params requestsList: A list object of `requestORMs` to format
    :return: A list of formated `requestORM` objects
    """
    requests = []
    for request in requestsList:
        requests.append(formatRequest(request))

    return requests


def formatRequest(request):
    """
    Same as above, however takes a single `requestORM` and formates the datetime

    :param requestg: The `requestORM` object of the tmpl to format
    :return:
    """
    request.formatedDate = datetime.strftime(request.created, "%a %b %d, %Y @ %H:%I%p")
    return request


class requestORM(Document):
    email = TextField()
    name = TextField()
    created = DateTimeField(default=datetime.now)
    docType = TextField(default="request")

    def save(self):
        self.store(db.couchServer)

    @classmethod
    def findByEmail(cls, email):
        request = cls.view(db.couchServer, 'typeViews/requestByEmail', key=email).rows[0]
        return request

    @classmethod
    def findByID(cls, ID):
        request = cls.load(db.couchServer, ID)
        return request
