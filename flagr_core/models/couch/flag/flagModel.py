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

import config.config as c
from models.couch.baseCouchModel import baseCouchModel
import models.couch.user.userModel as um
import utils.markdownUtils as mdu


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
    formatedDescription = ""
    formatedDate = ""
    author = ""

    def format(self):
        """
        Same as above, however takes a single `flagORM` and formates the datetime
        markdown.
        """
        self.formatedDescription = mdu.markClean(self.description)
        self.formatedDate = datetime.strftime(self.created, "%a %b %d, %Y @ %H:%I%p")
