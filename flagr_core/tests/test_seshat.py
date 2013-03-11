from webtest import TestApp
from webtest.app import AppError

import nose.tools as nst

import seshat.framework as seshat


class test_seshat(object):
    def setup(self):
        self.app = TestApp(seshat.app)

    def teardown(self):
        del self.app

    @nst.with_setup(setup, teardown)
    @nst.raises(AppError)
    def seshat_test_404(self):
        """
        Should raise a 404 AppError in webtest
        """
        self.app.get('/')

    def seshat_test_routing(self):
        pass
