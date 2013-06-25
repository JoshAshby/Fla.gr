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

from models.couch.baseCouchModel import baseCouchModel

import utils.signerUtils as su


class requestORM(Document, baseCouchModel):
    _name = "requests"
    email = TextField()
    created = DateTimeField(datetime.now())
    granted = DateTimeField()
    docType = TextField(default="request")
    _view = 'typeViews/request'

    def generateToken(self):
        """
        Generates an invite token to be sent to and used for registering,
        along with saves the time the request was granted.

        :return: The invite token which is a URL save, serialized version of
            their email signed with a secret and a salt.
        """
        token = su.requestToken(self.email)
        self.granted = datetime.now()
        self.save()
        return token

    def format(self):
        """
        Same as above, however takes a single `requestORM` and formates the datetime

        :param request: The `requestORM` object of the tmpl to format
        :return:
        """
        if self.granted:
            self.formatedGranted = datetime.strftime(self.granted, "%b %d, %Y")
        self.formatedCreated = datetime.strftime(self.created, "%b %d, %Y")

    @staticmethod
    def _search(items, value):
        """
        Searches the list `items` for the given value

        :param items: A list of ORM objects to search
        :param value: The value to search for, in this case
            value can be an email, or an id

        :return: Either None if no request was found, or the `requestORM`
            instance of the request
        """
        foundrequest = []
        for request in items:
            if request.email == value or request.id == value:
                foundrequest.append(request)
        if not foundrequest:
            return None
        else:
            request = foundrequest[0]
            return request

