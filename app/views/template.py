#!/usr/bin/env python
"""
TEMPLATE ALL THE THINGS WITH HANDLEBARS!!!!
Uses Pybars which is a python implimentation of handlebars which is an extension
of the mustache templating language to make a base template object by which is
easy to work with in the controllers.

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
import pystache
import os

tmplPath = os.path.dirname(__file__)+"/mustache/"


tmpls = {}
with open(tmplPath+"base.mustache", "r") as baseFile:
    base = unicode(baseFile.read())
baseFile.close()
tmpls["base"] = base


for directory in ["flagpole", "public", "error", "partials"]:
    tempTmpls = {}
    for folder in os.walk(tmplPath + directory + "/"):
        allTmpls = folder[2] # files in current directory
        where = folder[0].split(tmplPath)[1].rstrip("/") # relative folder path

        # Everytime we have files in the current directory, go through and see
        # if any are mustache template files, and if they are then read them into
        # memory and add them to the watcher
        for tmpl in allTmpls:
            parts = tmpl.split(".")
            name = parts[0]
            extension = parts[len(parts)-1]
            if extension != "mustache":
                continue

            fileBit = folder[0]+"/"+tmpl
            with open(fileBit, "r") as openTmpl:
                template = unicode(openTmpl.read())
            openTmpl.close()
            tempTmpls[where+"/"+name] = template

    tmpls.update(tempTmpls)


class template(object):
    def __init__(self, template, data):
        self._baseData = {
            "req": data,
            "stylesheets": [],
            "scripts": [],
            "static": "/static",
            "bootstrapCSS": "bootstrap.css",
            "breadcrumbs": ""
        }

        self._render = u""
        self.raw = u""

        self._template = template
        self._base = "base"

    @property
    def skeleton(self):
        return self._base

    @skeleton.setter
    def skeleton(self, value):
        assert type(value) == str
        self._base = value

    @skeleton.deleter
    def skeleton(self):
        self._base = "base"

    @property
    def data(self):
        return self._baseData

    @data.setter
    def data(self, value):
        assert type(value) == dict
        self._baseData.update(value)

    @property
    def scripts(self):
        return self._baseData["scripts"]

    @scripts.setter
    def scripts(self, value):
        assert type(value) == list
        self._baseData["scripts"].extend(value)

    @scripts.deleter
    def scripts(self):
        self._baseData["scripts"] = []

    @property
    def stylesheets(self):
        return self._baseData["stylesheets"]

    @stylesheets.setter
    def stylesheets(self, value):
        assert type(value) == list
        self._baseData["stylesheets"].extend(value)

    @stylesheets.deleter
    def stylesheets(self):
        self._baseData["stylesheets"] = []

    def partial(self, placeholder, template, data):
        data.update(self._baseData)
        self._data[placeholder] = pystache.render(template, data)

    def render(self):
        if "flagpole" in self._template.split("/"):
            self._baseData.update({
              "classes": {
                "navbar": "navbar-inverse"
              },
              "bootstrapCSS": "adminBootstrap.css"
            })
        body = self.raw
        if not self.raw:
            body = tmpls[self._template]

        body = pystache.render(body, self._baseData)

        _data = self._baseData
        _data.update({
            "body"  : body,
        })

        _data["req"].session.renderAlerts()

        self._render = pystache.render(tmpls[self._base], _data)

        return unicode(self._render)

    def __str__(self):
        return unicode(self._render)


def listView(template, collection):
    rendered = u""
    for item in collection:
      rendered += pystache.render(tmpls[template], {"row": item})

    return rendered

def paginateView(collection, template="partials/paginate"):
    if collection.pages > 2:
        previous = (collection.currentPage-1) if (collection.currentPage > 1) else False

        pages = []
        for page in range(1, (collection.pages+1)):
            pageDict = {"number": page}
            if page == collection.currentPage:
                pageDict.update({"class": "active"})
            pages.append(pageDict)

        last = (collection.currentPage+1) if collection.hasNextPage else False

        data = {"previous": previous,
            "pages": pages,
            "perpage": collection.perPage,
            "next": last,
            "last": collection.pages}

        return unicode(pystache.render(tmpls[template], data))

    else:
        return ""
