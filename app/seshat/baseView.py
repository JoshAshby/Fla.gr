#!/usr/bin/env python
"""
Seshat
Web App/API framework built on top of gevent
response container

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c


class baseView(object):
        """
        baseView

        Abstract:
                Very base view object. provides the
                standard interface for making views

        Accepts:

        Returns:
                str - String of HTML which represents a HTML page

        """
        def __init__(self):
                pass

        def build(self):
                """
                Over ride this
                """

        def __repr__(self):
                self.build()
                return str(self.returnHTML)

        def __str__(self):
                self.build()
                return str(self.returnHTML)

        def __unicode__(self):
                self.build()
                return u"%s" % str(self.returnHTML)

        def __getattr__(self, item):
                return object.__getattribute__(self, item)

        def __getitem__(self, item):
                return object.__getattribute__(self, item)

        def __setattr__(self, item, value):
                return object.__setattr__(self, item, value)

        def __setitem__(self, item, value):
                return object.__setattr__(self, item, value)


class baseHTMLView(baseView):
        """
        baseHTMLPage

        Abstract:
                Very base page for making bootstrap supported HTML5 pages

        Accepts:

        Returns:
                str - String of HTML which represents a HTML page

        """
        def __init__(self):
                self.assetURL = c.assetURL
                self.baseURL = c.baseURL
                self.title = ""
                self.body = ""
                self.scripts = ""
                self.css = ""
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
                %(body)s
                <script src="http://code.jquery.com/jquery-latest.js"></script>
                <script src="%(assetURL)s/js/bootstrap.js"></script>
                <script src="http://twitter.github.com/bootstrap/assets/js/bootstrap-carousel.js"></script>
                <script src="http://twitter.github.com/bootstrap/assets/js/bootstrap-tooltip.js"></script>
                %(scripts)s
        </body>
</html>""" % self

                return self.returnHTML

