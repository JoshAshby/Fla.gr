#!/usr/bin/env python
"""
fla.gr controller for editing users settings

For more information, see: https://github.com/JoshAshby/

http://xkcd.com/353/

Josh Ashby
2013
http://joshashby.com
joshuaashby@joshashby.com
"""
from seshat.route import route
from utils.baseHTMLObject import baseHTMLObject

from views.you.youSettingsTmpl import youSettingsTmpl

import bcrypt


@route("/your/settings")
class youSettings(baseHTMLObject):
    __name__ = "settings"
    __login__ = True
    def GET(self):
        """
        """
        view = youSettingsTmpl(searchList=[self.tmplSearchList])

        return view

    def POST(self):
        passwordCurrent = self.env["members"]["passwordCurrent"] if self.env["members"].has_key("passwordCurrent") else None
        password = self.env["members"]["password"] if self.env["members"].has_key("password") else None
        passwordTwice = self.env["members"]["passwordTwice"] if self.env["members"].has_key("passwordTwice") else None
        about = self.env["members"]["about"] or ""
        email = self.env["members"]["email"] or ""
        emailVis = True if self.env["members"].has_key("emailVis") else False

        self.session.about = about
        self.session.email = email
        self.session.emailVisibility = emailVis
        self.session.save()

        if password and passwordTwice and passwordCurrent:
            if bcrypt.hashpw(passwordCurrent, self.session.password) == self.session.password:
                if password == passwordTwice:
                    self.session.setPassword(password)

                else:
                    view = youSettingsTmpl(searchList=[self.tmplSearchList])
                    view.passwordMatchError = True

                    self.session.alerts = self.session.HTMLAlert("Those passwords don't match, please try again.", "", "error")

                    return view
            else:
                view = youSettingsTmpl(searchList=[self.tmplSearchList])
                view.passwordError = True

                self.session.alerts = self.session.HTMLAlert("We're sorry but your current password appeard to be entered wrong. Please try again.", "", "error")

                return view

        self.session.alerts = self.session.HTMLAlert("Settings updated", "Yay", "success")

        self.head = ("303 SEE OTHER",
            [("location", "/your/dashboard")])
