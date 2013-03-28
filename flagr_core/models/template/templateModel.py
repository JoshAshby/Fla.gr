#!/usr/bin/env python
"""
fla.gr template model for email and pages templates
"""
from couchdb.mapping import Document, TextField, DateTimeField
from datetime import datetime

from models.baseModel import baseCouchModel
import utils.markdownUtils as mdu


def formatTmpls(tmplsList):
    """
    Takes a list of `templateORM`s and formates the datetime and markdown
    for templates.

    :params tmplList: A list object of `templateORMs` to format
    :typetmplList: List
    :return: A list of formated `templateORM` objects
    :rtype: List
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
    :return: the tmpl with the template and date formated
    :rtype: templateORM
    """
    tmpl.formatedTemplate = mdu.mark(tmpl.template)
    tmpl.formatedDate = datetime.strftime(tmpl.created, "%a %b %d, %Y @ %H:%I%p")
    return tmpl


class templateORM(Document, baseCouchModel):
    _view = "viewTypes/template"
    name = TextField()
    description = TextField()
    template = TextField()
    created = DateTimeField(default=datetime.now)
    docType = TextField(default="tmpl")
    type = TextField()
    userID = TextField()
    formatedDate = ""
