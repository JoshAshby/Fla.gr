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

basic_urls = []


@route("/basic", basic_urls)
class basic(baseHTTPObject):
    """
    Returns a basic page, and response codes for various
    """
    def GET(self):
        self.head = ("200 OK", [("Content-Type", "text/html")])

        return """
<html>
    <head>
        <title>Test page</title>
    </head>
    <body>
        This is a test HTML page body
    </body>
</html>
"""

    def POST(self):
        self.head = ("201 CREATED", [("Location", "/basic")])

    def PUT(self):
        self.head = ("405 NOT ALLOWED", [("Allow", "GET,POST"),
            ("Content-Type", "text/plain")])
        return "This isn't allowed"

    def DELETE(self):
        self.head = ("303 SEE OTHER", [("Location", "/basic")])


class test_seshat_base(object):
    """
    Tests basic routing and the GET POST PUT and DELETE methods
    """
    @classmethod
    def setup_class(cls):
        cls.app = TestApp(seshat.app)
        seshat.c.urls = basic_urls

    @classmethod
    def teardown_class(cls):
        del(cls.app)

    def seshat_test_get(self):
        """
        Tests the GET method of the baseHTTPObject in Seshat
        """
        get_reply = self.app.get('/basic')

        print "Make sure the status code is good..."
        assert get_reply.status == "200 OK"

        print "Content length is good, and type is proper"
        assert get_reply.content_type == "text/html"
        assert get_reply.content_length > 0

        print "Make sure the content is the same as we expect..."
        assert get_reply.normal_body.replace(" ", "") == ("""<html><head><title>Test page</title></head><body>This is a test HTML page body</body></html>""").replace(" ", "")

    def seshat_test_post(self):
        """
        Should return with a 201 CREATED header, and a location
        """
        post_reply = self.app.post('/basic')

        assert post_reply.status == "201 CREATED"

    @nst.raises(AppError)
    def seshat_test_put(self):
        """
        Should return with a 405 NOT ALLOWED
        """
        put_reply = self.app.put('/basic')

        assert put_reply.status == "405 NOT ALLOWED"

        print put_reply
        assert put_reply.normal_body == "This isn't allowed"

    def seshat_test_delete(self):
        """
        Should return a 303 SEE OTHER which we'll follow back to /basic
        """
        delete_reply = self.app.delete('/basic')

        assert delete_reply.status == "303 SEE OTHER"

        follow = delete_reply.follow()

        assert follow.status == "200 OK"
