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

from models.couch.baseCouchModel import baseCouchModel
import utils.markdownUtils as mdu
import models.couch.flag.collections.userFlagCollection as fc
import models.couch.flag.collections.userPublicFlagCollection as pubfc


class flagORM(Document, baseCouchModel):
    _view = "typeViews/flag"
    _name = "flags"
    userID = TextField()
    title = TextField()
    description = TextField()
    url = TextField()
    labels = ListField(TextField())
    visibility = BooleanField(default=False)
    created = DateTimeField(default=datetime.now)
    docType=TextField(default="flag")
    reported = BooleanField(default=False)

    def format(self):
        """
        Same as above, however takes a single `flagORM` and formates the datetime
        markdown.
        """
        self.formatedDescription = mdu.markClean(self.description)
        self.formatedDate = datetime.strftime(self.created, "%a %b %d, %Y @ %H:%I%p")

    def collectionsUpdate(self):
        pubFlags = pubfc.userPublicFlagsCollection(self.userID)
        if self.visibility:
            pubFlags.addObject(self.id)
        else:
            pubFlags.delObject(self.id)

    def collectionsDelete(self):
        privFlags = fc.userFlagsCollection(self.session.id)
        pubFlags = pubfc.userPublicFlagsCollection(self.userID)

        privFlags.delObject(self.id)
        pubFlags.delObject(self.id)
