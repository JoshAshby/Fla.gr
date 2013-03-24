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

from models.baseModel import baseCouchModel

import utils.signerUtils as su


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

    :param request: The `requestORM` object of the tmpl to format
    :return:
    """
    if request.granted:
        request.formatedGranted = datetime.strftime(request.granted, "%b %d, %Y")
    request.formatedCreated = datetime.strftime(request.created, "%b %d, %Y")
    return request


class requestORM(Document, baseCouchModel):
    email = TextField()
    created = DateTimeField()
    granted = DateTimeField()
    docType = TextField(default="request")

    @classmethod
    def new(cls, email):
        return cls(email=email, created=datetime.now())

    def generateToken(self):
        """
        
        """
        token = su.requestToken(self.email)
        self.granted = datetime.now()
        self.save()
        return token

    @classmethod
    def all(cls):
        return cls.getAll('typeViews/request')

    @classmethod
    def find(cls, value):
        """
        Searches couchdb for documents that have the requested email or

        :param value: The value to search for in the ORM
        :return: Either a `cls` instance or a list of `cls` instances
            if a result or multiple have been found.
            `None` if no user is found
        """
        return cls.findWithView('typeViews/request', value)


    @staticmethod
    def _search(items, value):
        """
        Searches the list `items` for the given value

        :param items: A list of ORM objects to search
        :param value: The value to search for, in this case
            value can be an email, or an id
        """
        foundUser = []
        for user in items:
            if user.email == value or user.id == value:
                foundUser.append(user)
        if not foundUser:
            return None
        else:
            user = foundUser[0]
            return user

