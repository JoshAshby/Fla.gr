#!/usr/bin/env python
"""
fla.gr template model for email and pages templates

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


class templateORM(Document):
    name = TextField()
    template = TextField()
    created = DateTimeField(default=datetime.now)
    docType = TextField(default="tmpl")
    author = TextField(default="")

    def save(self):
        self.store(db.couchServer)
