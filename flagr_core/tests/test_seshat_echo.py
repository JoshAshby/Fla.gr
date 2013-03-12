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
from seshat.baseObject import baseHTTPObject

echo_urls = []


@route("/echo", echo_urls)
class getEcho(baseHTTPObject):
    """
    Returns a basic page, and response codes for various
    """
    def GET(self):
        echo = self.env["members"]["echo"]
        self.head = ("200 OK", [("Content-Type", "text/html")])

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
        self.head = ("405 NOT ALLOWED", [("Allow", "GET,POST"),
            ("Content-Type", "text/plain")])
        return "This isn't allowed"

    def PUT(self):
        self.head = ("405 NOT ALLOWED", [("Allow", "GET,POST"),
            ("Content-Type", "text/plain")])
        return "This isn't allowed"

    def DELETE(self):
        self.head = ("405 NOT ALLOWED", [("Allow", "GET,POST"),
            ("Content-Type", "text/plain")])
        return "This isn't allowed"


class test_seshat_echo(object):
    """
    Tests to make sure the query sting and other parameters get to the objects
    """
    @classmethod
    def setup_class(cls):
        cls.app = TestApp(seshat.app)
        seshat.c.urls = echo_urls

    @classmethod
    def teardown_class(cls):
        del(cls.app)

    def seshat_test_get_echo(self):
        """
        Sends "hello" and expects it to be echoed back in an HTML page through GET
        """
        test_param = "hello"
        echo_get_reply = self.app.get('/echo', {"echo": test_param})

        assert echo_get_reply.status == "200 OK"

        assert echo_get_reply.normal_body.replace(" ", "") == ("""<html><head><title>echo</title></head><body>%s</body></html>""" % test_param).replace(" ", "")

    @nst.raises(AppError)
    def seshat_test_post_echo(self):
        """
        AppError for the 405
        """
        echo_post_reply = self.app.post('/echo')

    @nst.raises(AppError)
    def seshat_test_put_echo(self):
        """
        AppError for the 405
        """
        echo_put_reply = self.app.post('/echo')

    @nst.raises(AppError)
    def seshat_test_delete_echo(self):
        """
        AppError for the 405
        """
        echo_delete_reply = self.app.post('/echo')
