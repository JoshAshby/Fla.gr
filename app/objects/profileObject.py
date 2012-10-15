#!/usr/bin/env python2
"""
Web App/API framework built on top of gevent
baseObject to build pages off of

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2012
http://joshashby.com
joshuaashby@joshashby.com
"""
import config as c

import objects.baseObject as bo
import views.pyStrap.pyStrap as ps


class profileObject(bo.baseHTTPPageObject):
       __login__ = True
       __name__ = "profile"
       def finishInit(self):
                messCount = c.session.mail.unreadCount()
                readCount = c.session.mail.readCount()
                if messCount:
                        messCounter = ps.baseBadge(ps.baseBadge(messCount, classes="badge-important") + " %s"%readCount, style="padding-left: 0px")
                else:
                        messCounter = ps.baseBadge(str(readCount))

                messages = "%s Your Messages %s" % (ps.baseIcon("envelope-alt"), messCounter)
                about = c.session.user["about"] or "You have nothing here yet!"

                self.view.sidebar = ps.baseWell(ps.baseNavList(items=[{"header": "Your stuff"},
                        {"link": c.baseURL + "/your/flags", "name": "%s Your flags"%ps.baseIcon("flag")},
                        {"link": c.baseURL + "/your/labels", "name": "%s Your labels"%ps.baseIcon("tags")},
                        "divider",
                        {"header": "Settings"},
                        {"link": c.baseURL+"/your/messages", "name": messages},
                        {"link": c.baseURL + "/your/settings", "name": "%s Your settings"%ps.baseIcon("cogs")},
                        "divider",
                        {"header": "About you (%s)"%c.session.user["username"]},
                        {"text": about}
                ]))
