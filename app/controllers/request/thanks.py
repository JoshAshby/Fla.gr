#!/usr/bin/env python
"""
fla.gr controller for displaying a thank you page after requesting an invite

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import autoRoute
from seshat.baseHTMLObject import baseHTMLObject


@autoRoute()
class thanks(baseHTMLObject):
    _title = "thanks!"
    _defaultTmpl = "public/request/thanks"
    def GET(self):
        """
        """
        if self.request.cfg.enableRequests:
            return self.view
        else:
            self._404()
