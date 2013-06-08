#!/usr/bin/env python
"""
fla.gr template model for email and pages templates

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from couchdb.mapping import Document, TextField, DateTimeField
from datetime import datetime

from models.couch.baseCouchModel import baseCouchModel
import utils.markdownUtils as mdu


def formatTmpls(tmplsList):
    """
    Takes a list of `templateORM`s and formates the datetime and markdown
    for templates.

    :params tmplList: A list object of `templateORMs` to format
    :return: A list of formated `templateORM` objects
    """
    tmpls = []
    for tmpl in tmplsList:
        tmpls.append(formatTmpl(tmpl))

    return tmpls


def formatTmpl(tmpl):
    """
    Same as above, however takes a single `templateORM` and formats the datetime
    markdown.

    :param tmpl: The `templateORM` object of the tmpl to format
    :return:
    """
    tmpl.formatedTemplate = mdu.mark(tmpl.template)
#    tmpl.formatedDate = datetime.strftime(tmpl.created, "%a %b %d, %Y @ %H:%I%p")
    return tmpl


class templateORM(Document, baseCouchModel):
    _name = "templates"
    name = TextField()
    description = TextField()
    template = TextField()
    created = DateTimeField(default=datetime.now)
    docType = TextField(default="tmpl")
    type = TextField()
    userID = TextField()
    formatedDate = ""
    _view = "typeViews/template"
