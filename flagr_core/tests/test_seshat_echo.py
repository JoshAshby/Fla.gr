#!/usr/bin/env python
"""
Test case for making sure that seshat is routing properly
and is capable of handling GET,POST,PUT and DELETE methods.
This indicates a very big problem, if one of these tests fails
because that indicates that the core of Seshat is broken
"""
from webtest import TestApp
from webtest.app import AppError

import nose.tools as nst

import seshat.coreApp as seshat

from seshat.route import route
from seshat.baseObject import baseHTTPObject

basic_echo_urls = []


@route("/echo", basic_echo_urls)
class basic_echo(baseHTTPObject):
    """
    Returns a basic page through GET which places one parameter from env["members"]
    into an HTML page, and returns 405 NOT ALLOWED for all other Methods
    """
    def GET(self):
        echo = self.env["members"]["echo"]
        self.head = ("200 OK", [("Content-Type", "text/plain")])

        return echo

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


class test_seshat_basic_echo(object):
    """
    Tests to make sure the query sting and other parameters get to the objects
    """
    @classmethod
    def setup_class(cls):
        """
        Make a new instance of the Seshat core app, and replace it's
        URL list with our own so this test's routing is isolated
        """
        cls.app = TestApp(seshat.app)
        seshat.c.urls = basic_echo_urls

        cls.url = "/echo"
        cls.params = {"echo": "hello"}

    @classmethod
    def teardown_class(cls):
        """
        Destroy the created Seshat core app instance
        """
        del(cls.app)

    def test_seshat_basic_echo_get(self):
        """
        Sends "hello" and expects it to be echoed back in an HTML page through GET
        """
        get_reply = self.app.get(self.url, self.params)

        assert get_reply.status == "200 OK"

        assert get_reply.normal_body.replace(" ", "") == ("""<html><head><title>echo</title></head><body>%s</body></html>""" % self.params["echo"]).replace(" ", "")

    @nst.raises(AppError)
    def test_seshat_basic_echo_post(self):
        """
        AppError for the 405 POST
        """
        post_reply = self.app.post(self.url)

        assert post_reply.status == "405 NOT ALLOWED"

    @nst.raises(AppError)
    def test_seshat_basic_echo_put(self):
        """
        AppError for the 405 PUT
        """
        put_reply = self.app.post(self.url)

        assert put_reply.status == "405 NOT ALLOWED"

    @nst.raises(AppError)
    def test_seshat_basic_echo_delete(self):
        """
        AppError for the 405 DELETE
        """
        delete_reply = self.app.post(self.url)

        assert delete_reply.status == "405 NOT ALLOWED"
