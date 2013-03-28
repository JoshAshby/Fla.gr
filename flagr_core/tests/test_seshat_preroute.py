#!/usr/bin/env python
"""
Test case for making sure that seshat is still working and responding
with a 404 for not found pages. If this fails then all hell is probably
about to, or has, broken loose.
"""
from webtest import TestApp
from webtest.app import AppError

import nose.tools as nst

import seshat.coreApp as seshat


class test_seshat_preroute(object):
    """
    Pre routing should result in a defult 404 NOT FOUND error
    """
    def setup(self):
        self.app = TestApp(seshat.app)

    def teardown(self):
        del(self.app)

    @nst.with_setup(setup, teardown)
    @nst.raises(AppError)
    def seshat_test_404(self):
        """
        Should raise a 404 AppError in webtest
        """
        self.app.get('/')
