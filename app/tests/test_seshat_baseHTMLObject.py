#!/usr/bin/env python
"""
Test case for making sure that seshat is routing properly
and is capable of handling GET,POST,PUT and DELETE methods.
This indicates a very big problem, if one of these tests fails
because that indicates that the core of Seshat is broken

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from webtest import TestApp
from webtest.app import AppError

import nose.tools as nst

import seshat.coreApp as seshat

from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

htmlObj_urls = []


@route("/html/echo", htmlObj_urls)
class htmlObj_echo(baseHTMLObject):
    """
    Returns a basic page through GET which places one parameter from env["members"]
    into an HTML page, and returns 405 NOT ALLOWED for all other Methods
    """
    def GET(self):
        echo = self.env["members"]["echo"]

        return """
<html>
    <head>
        <title>echo</title>
    </head>
    <body>
        %s
    </body>
</html>
""" % echo

    def POST(self):
        """
        Replace with test code
        """
        self.head = ("405 NOT ALLOWED", [("Allow", "GET,POST"),
            ("Content-Type", "text/plain")])
        return "This isn't allowed"

    def PUT(self):
        """
        Replace with test code
        """
        self.head = ("405 NOT ALLOWED", [("Allow", "GET,POST"),
            ("Content-Type", "text/plain")])
        return "This isn't allowed"

    def DELETE(self):
        """
        Replace with test code
        """
        self.head = ("405 NOT ALLOWED", [("Allow", "GET,POST"),
            ("Content-Type", "text/plain")])
        return "This isn't allowed"


class test_seshat_htmlObj(object):
    """
    """
    @classmethod
    def setup_class(cls):
        """
        Make a new instance of the Seshat core app, and replace it's
        URL list with our own so this test's routing is isolated
        """
        cls.app = TestApp(seshat.app)
        seshat.c.urls = htmlObj_urls

        cls.url = "/html/echo"
        cls.params = {"echo": "hello"}

    @classmethod
    def teardown_class(cls):
        """
        Destroy the created Seshat core app instance
        """
        del(cls.app)

    def test_seshat_htmlObj_get(self):
        """
        """
        get_reply = self.app.get(self.url, self.params)

        assert get_reply.status == "200 OK"

    @nst.raises(AppError)
    def test_seshat_htmlObj_post(self):
        """
        AppError for the 405 POST
        """
        post_reply = self.app.post(self.url)

        assert post_reply.status == "405 NOT ALLOWED"

    @nst.raises(AppError)
    def test_seshat_htmlObj_put(self):
        """
        AppError for the 405 PUT
        """
        put_reply = self.app.put(self.url)

        assert put_reply.status == "405 NOT ALLOWED"

    @nst.raises(AppError)
    def test_seshat_htmlObj_delete(self):
        """
        AppError for the 405 DELETE
        """
        delete_reply = self.app.delete(self.url)

        assert delete_reply.status == "405 NOT ALLOWED"
