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


for directory in ["flagpole", "public", "error"]:
    tempTmpls = {}
    for folder in os.walk(tmplPath + directory + "/"):
        allTmpls = folder[2] # files in current directory
        where = folder[0].split(tmplPath)[1].rstrip("/") # relative folder path

        # Everytime we have files in the current directory, go through and see
        # if any are mustache template files, and if they are then read them into
        # memory and add them to the watcher
        for tmpl in allTmpls:
            name, extension = tmpl.split(".")
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
            "bootstrapCSS": "bootstrap.css"
        }

        self._render = u""
        self.raw = u""

        self._template = template

    @property
    def data(self):
        return self._baseData

    @data.setter
    def data(self, value):
        if type(value) != dict:
            raise Exception("Data must be of type dict")
        self._baseData.update(value)

    def partial(self, placeholder, template, data):
        data.update(self._baseData)
        self._data[placeholder] = pystache.render(template, data)

    def render(self):
        body = self.raw
        if not self.raw:
            body = tmpls[self._template]

        body = pystache.render(body, self._baseData)

        self._data = self._baseData
        self._data.update({
            "body"  : body,
        })

        self._data["req"].session.renderAlerts()

        self._render = pystache.render(tmpls["base"], self._data)

        return unicode(self._render)

    def __str__(self):
        return unicode(self._render)
