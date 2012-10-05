#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
base HTML page template

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c


class basePage(object):
        """
        basePage

        Abstract:
                Very base page for flagr

        Accepts:
                content
                title


        Returns:
                str - String of HTML which represents a HTML page

        """
        def __init__(self, title="", content=""):
                self.assetURL = c.assetURL
                self.baseURL = c.baseURL
                self.title = title
                self.content = content
                self.returnHTML = ""

        def build(self):
                self.returnHTML = """<!DOCTYPE html>
<html>
        <head>
                <title>%(title)s</title>
                <!-- Bootstrap -->
                <link href="%(assetURL)s/css/bootstrap.min.css" rel="stylesheet">
                <link rel="stylesheet" href="%(assetURL)s/css/font-awesome.css">
        </head>
        <body>
                %(content)s
                <script src="http://code.jquery.com/jquery-latest.js"></script>
                <script src="%(assetURL)s/js/bootstrap.js"></script>
        </body>
</html>""" % self

        def __repr__(self):
                self.build()
                return str(self.returnHTML)

        def __str__(self):
                self.build()
                return str(self.returnHTML)

        def __unicode__(self):
                self.build()
                return u"%s" % str(self.returnHTML)

        def __add__(self, other):
                self.build()
                return str(self.returnHTML)+other

        def __radd__(self, other):
                self.build()
                return other+str(self.returnHTML)

        def __getattr__(self, item):
                return object.__getattribute__(self, item)

        def __getitem__(self, item):
                return object.__getattribute__(self, item)

        def __setattr__(self, item, value):
                return object.__setattr__(self, item, value)

        def __setitem__(self, item, value):
                return object.__setattr__(self, item, value)
