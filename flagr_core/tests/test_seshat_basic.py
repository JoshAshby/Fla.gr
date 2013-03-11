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

import nose.tools as nst

import seshat.coreApp as seshat

from seshat.route import route
from seshat.baseObject import baseHTTPObject

@route("/basic")
class baic(baseHTTPObject):
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
        pass

    def PUT(self):
        pass

    def DELETE(self):
        pass


class test_seshat_base(object):
    """
    """
    def setup(self):
        self.app = TestApp(seshat.app)

    def teardown(self):
        del(self.app)

    @nst.with_setup(setup, teardown)
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

    @nst.with_setup(setup, teardown)
    def seshat_test_post(self):
        pass

    @nst.with_setup(setup, teardown)
    def seshat_test_put(self):
        pass

    @nst.with_setup(setup, teardown)
    def seshat_test_delete(self):
        pass
